"""
招聘方案相关的Pydantic模型
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from .job import Job
from .user import User

class PlanBase(BaseModel):
    """招聘方案基础模型"""
    title: str = Field(..., description="方案标题")
    job_id: int = Field(..., description="职位ID")
    description: Optional[str] = Field(None, description="方案描述")
    strategy: Optional[str] = Field(None, description="招聘策略")
    candidate_ids: Optional[List[int]] = Field(None, description="候选人ID列表")

class PlanCreate(PlanBase):
    """创建招聘方案模型"""
    pass

class PlanUpdate(BaseModel):
    """更新招聘方案模型"""
    title: Optional[str] = Field(None, description="方案标题")
    description: Optional[str] = Field(None, description="方案描述")
    strategy: Optional[str] = Field(None, description="招聘策略")
    candidate_ids: Optional[List[int]] = Field(None, description="候选人ID列表")

class PlanInDB(PlanBase):
    """数据库中的招聘方案模型"""
    id: int
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class Plan(PlanInDB):
    """招聘方案响应模型"""
    job: Optional[Job] = None
    creator: Optional[User] = None
