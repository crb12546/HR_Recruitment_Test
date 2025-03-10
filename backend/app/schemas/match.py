"""
匹配相关的Pydantic模型
"""
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from .job import Job
from .resume import Resume

class MatchBase(BaseModel):
    """匹配基础模型"""
    resume_id: int = Field(..., description="简历ID")
    job_id: int = Field(..., description="职位ID")
    match_score: float = Field(..., description="匹配分数")
    match_explanation: Optional[str] = Field(None, description="匹配说明")

class MatchCreate(MatchBase):
    """创建匹配模型"""
    pass

class MatchInDB(MatchBase):
    """数据库中的匹配模型"""
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class Match(MatchInDB):
    """匹配响应模型"""
    resume: Optional[Resume] = None
    job: Optional[Job] = None
