"""
招聘方案模型
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Plan(Base):
    """招聘方案模型类"""
    __tablename__ = "plans"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False, comment="方案标题")
    job_id = Column(Integer, ForeignKey("job_requirements.id"), nullable=False, comment="职位ID")
    description = Column(Text, comment="方案描述")
    strategy = Column(Text, comment="招聘策略")
    candidate_ids = Column(JSON, comment="候选人ID列表")
    created_by = Column(Integer, ForeignKey("users.id"), comment="创建人ID")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
    # 关系
    job = relationship("JobRequirement", foreign_keys=[job_id])
    creator = relationship("User", foreign_keys=[created_by])
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "title": self.title,
            "job_id": self.job_id,
            "description": self.description,
            "strategy": self.strategy,
            "candidate_ids": self.candidate_ids,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "job": self.job.to_dict() if self.job else None,
            "creator": self.creator.to_dict() if self.creator else None
        }
