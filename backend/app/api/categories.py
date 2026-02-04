from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.core.security import get_current_admin
from app.models.category import Category
from app.models.article import Article
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse

router = APIRouter()


@router.get("", response_model=List[CategoryResponse])
async def get_categories(db: AsyncSession = Depends(get_db)):
    # Get categories with article count
    query = select(
        Category,
        func.count(Article.id).label("article_count")
    ).outerjoin(Article, Article.category_id == Category.id).group_by(Category.id)
    
    result = await db.execute(query)
    categories = []
    for row in result:
        cat = row[0]
        cat.article_count = row[1]
        categories.append(cat)
    return categories


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    
    # Get article count
    count_result = await db.execute(
        select(func.count(Article.id)).where(Article.category_id == category_id)
    )
    category.article_count = count_result.scalar() or 0
    return category


@router.post("", response_model=CategoryResponse)
async def create_category(
    category_data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    slug = category_data.slug or category_data.name.lower().replace(" ", "-")
    
    # Check if name exists
    result = await db.execute(select(Category).where(Category.name == category_data.name))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="分类名称已存在")
    
    category = Category(
        name=category_data.name,
        slug=slug,
        description=category_data.description
    )
    db.add(category)
    await db.flush()
    await db.refresh(category)
    category.article_count = 0
    return category


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    
    update_data = category_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(category, field, value)
    
    await db.flush()
    await db.refresh(category)
    
    # Get article count
    count_result = await db.execute(
        select(func.count(Article.id)).where(Article.category_id == category_id)
    )
    category.article_count = count_result.scalar() or 0
    return category


@router.delete("/{category_id}")
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    
    # Check if category has articles
    count_result = await db.execute(
        select(func.count(Article.id)).where(Article.category_id == category_id)
    )
    if count_result.scalar() > 0:
        raise HTTPException(status_code=400, detail="该分类下有文章，无法删除")
    
    await db.delete(category)
    return {"message": "删除成功"}
