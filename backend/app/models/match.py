"""
简历与职位匹配模型
"""
from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Match(Base):
    """简历与职位匹配模型类"""
    __tablename__ = "matches"
    
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False, comment="简历ID")
    job_id = Column(Integer, ForeignKey("job_requirements.id"), nullable=False, comment="职位ID")
    match_score = Column(Float, nullable=False, comment="匹配分数")
    match_explanation = Column(Text, comment="匹配说明")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    
    # 关系
    resume = relationship("Resume", foreign_keys=[resume_id])
    job = relationship("JobRequirement", foreign_keys=[job_id])
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "resume_id": self.resume_id,
            "job_id": self.job_id,
            "match_score": self.match_score,
            "match_explanation": self.match_explanation,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "resume": self.resume.to_dict() if self.resume else None,
            "job": self.job.to_dict() if self.job else None
        }
