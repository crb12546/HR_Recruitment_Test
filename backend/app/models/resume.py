"""
简历模型
"""
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base
from .tag import resume_tag

class Resume(Base):
    """简历模型类"""
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_name = Column(String(50), nullable=False, comment="候选人姓名")
    file_url = Column(String(255), nullable=False, comment="文件URL")
    file_type = Column(String(20), nullable=False, comment="文件类型")
    ocr_content = Column(Text, comment="OCR识别内容")
    parsed_content = Column(Text, comment="解析后内容")
    talent_portrait = Column(Text, comment="人才画像")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
    # 与标签的多对多关系
    tags = relationship("Tag", secondary=resume_tag, back_populates="resumes")
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "candidate_name": self.candidate_name,
            "file_url": self.file_url,
            "file_type": self.file_type,
            "ocr_content": self.ocr_content,
            "parsed_content": self.parsed_content,
            "talent_portrait": self.talent_portrait,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "tags": [tag.to_dict() for tag in self.tags] if self.tags else []
        }
