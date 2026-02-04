from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.core.security import get_current_admin
from app.models.tag import Tag
from app.models.article import article_tags
from app.models.user import User
from app.schemas.tag import TagCreate, TagUpdate, TagResponse

router = APIRouter()


@router.get("", response_model=List[TagResponse])
async def get_tags(db: AsyncSession = Depends(get_db)):
    # Get tags with article count
    query = select(
        Tag,
        func.count(article_tags.c.article_id).label("article_count")
    ).outerjoin(article_tags, article_tags.c.tag_id == Tag.id).group_by(Tag.id)
    
    result = await db.execute(query)
    tags = []
    for row in result:
        tag = row[0]
        tag.article_count = row[1]
        tags.append(tag)
    return tags


@router.get("/{tag_id}", response_model=TagResponse)
async def get_tag(tag_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tag).where(Tag.id == tag_id))
    tag = result.scalar_one_or_none()
    if not tag:
        raise HTTPException(status_code=404, detail="标签不存在")
    
    # Get article count
    count_result = await db.execute(
        select(func.count(article_tags.c.article_id)).where(article_tags.c.tag_id == tag_id)
    )
    tag.article_count = count_result.scalar() or 0
    return tag


@router.post("", response_model=TagResponse)
async def create_tag(
    tag_data: TagCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    slug = tag_data.slug or tag_data.name.lower().replace(" ", "-")
    
    # Check if name exists
    result = await db.execute(select(Tag).where(Tag.name == tag_data.name))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="标签名称已存在")
    
    tag = Tag(
        name=tag_data.name,
        slug=slug,
        color=tag_data.color
    )
    db.add(tag)
    await db.flush()
    await db.refresh(tag)
    tag.article_count = 0
    return tag


@router.put("/{tag_id}", response_model=TagResponse)
async def update_tag(
    tag_id: int,
    tag_data: TagUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    result = await db.execute(select(Tag).where(Tag.id == tag_id))
    tag = result.scalar_one_or_none()
    if not tag:
        raise HTTPException(status_code=404, detail="标签不存在")
    
    update_data = tag_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(tag, field, value)
    
    await db.flush()
    await db.refresh(tag)
    
    # Get article count
    count_result = await db.execute(
        select(func.count(article_tags.c.article_id)).where(article_tags.c.tag_id == tag_id)
    )
    tag.article_count = count_result.scalar() or 0
    return tag


@router.delete("/{tag_id}")
async def delete_tag(
    tag_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    result = await db.execute(select(Tag).where(Tag.id == tag_id))
    tag = result.scalar_one_or_none()
    if not tag:
        raise HTTPException(status_code=404, detail="标签不存在")
    
    await db.delete(tag)
    return {"message": "删除成功"}
