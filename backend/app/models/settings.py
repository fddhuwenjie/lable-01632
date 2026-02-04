from sqlalchemy import Column, Integer, String, Text

from app.core.database import Base


class SiteSettings(Base):
    __tablename__ = "site_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    site_name = Column(String(100), default="My Blog", nullable=False)
    site_description = Column(Text, nullable=True)
    site_keywords = Column(String(500), nullable=True)
    author_name = Column(String(100), nullable=True)
    author_bio = Column(Text, nullable=True)
    author_avatar = Column(String(500), nullable=True)
    github_url = Column(String(200), nullable=True)
    email = Column(String(100), nullable=True)
