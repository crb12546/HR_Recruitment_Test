"""
标签模型
"""
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

# 简历-标签多对多关系表
resume_tag = Table(
    "resume_tag",
    Base.metadata,
    Column("resume_id", Integer, ForeignKey("resumes.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)
)

class Tag(Base):
    """标签模型类"""
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True, comment="标签名称")
    category = Column(String(20), comment="标签类别")
    
    # 与简历的多对多关系
    resumes = relationship("Resume", secondary=resume_tag, back_populates="tags")
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category
        }
