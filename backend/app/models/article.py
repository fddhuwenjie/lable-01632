from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Table, Enum
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


# Many-to-many relationship table
article_tags = Table(
    'article_tags',
    Base.metadata,
    Column('article_id', Integer, ForeignKey('articles.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
)


class ArticleStatus(str, enum.Enum):
    draft = "draft"
    published = "published"


class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    summary = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    cover_image = Column(String(500), nullable=True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    status = Column(String(20), default="draft", nullable=False)
    views = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    category = relationship("Category", back_populates="articles")
    author = relationship("User", back_populates="articles")
    tags = relationship("Tag", secondary=article_tags, backref="articles")
