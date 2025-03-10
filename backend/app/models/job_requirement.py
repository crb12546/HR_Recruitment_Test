"""
招聘需求模型
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from datetime import datetime
from app.db.base import Base

class JobRequirement(Base):
    """招聘需求模型类"""
    __tablename__ = "job_requirements"
    
    id = Column(Integer, primary_key=True, index=True)
    position_name = Column(String(100), nullable=False, comment="职位名称")
    department = Column(String(50), comment="部门")
    responsibilities = Column(Text, nullable=False, comment="职责描述")
    requirements = Column(Text, nullable=False, comment="职位要求")
    salary_range = Column(String(50), comment="薪资范围")
    location = Column(String(100), comment="工作地点")
    tags = Column(JSON, nullable=True, comment="职位标签")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "position_name": self.position_name,
            "department": self.department,
            "responsibilities": self.responsibilities,
            "requirements": self.requirements,
            "salary_range": self.salary_range,
            "location": self.location,
            "tags": self.tags,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
