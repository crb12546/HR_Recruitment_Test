"""
招聘需求相关的Pydantic模型
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class JobBase(BaseModel):
    """招聘需求基础模型"""
    position_name: str = Field(..., description="职位名称")
    department: Optional[str] = Field(None, description="部门")
    responsibilities: str = Field(..., description="职责描述")
    requirements: str = Field(..., description="职位要求")
    salary_range: Optional[str] = Field(None, description="薪资范围")
    location: Optional[str] = Field(None, description="工作地点")
    tags: Optional[List[str]] = Field(None, description="职位标签")

class JobCreate(JobBase):
    """创建招聘需求模型"""
    pass

class JobUpdate(BaseModel):
    """更新招聘需求模型"""
    position_name: Optional[str] = Field(None, description="职位名称")
    department: Optional[str] = Field(None, description="部门")
    responsibilities: Optional[str] = Field(None, description="职责描述")
    requirements: Optional[str] = Field(None, description="职位要求")
    salary_range: Optional[str] = Field(None, description="薪资范围")
    location: Optional[str] = Field(None, description="工作地点")
    tags: Optional[List[str]] = Field(None, description="职位标签")

class JobInDB(JobBase):
    """数据库中的招聘需求模型"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class Job(JobInDB):
    """招聘需求响应模型"""
    pass

class JobParseResult(BaseModel):
    """招聘需求解析结果模型"""
    position_name: Optional[str] = Field(None, description="职位名称")
    department: Optional[str] = Field(None, description="部门")
    responsibilities: Optional[str] = Field(None, description="职责描述")
    requirements: Optional[str] = Field(None, description="职位要求")
    salary_range: Optional[str] = Field(None, description="薪资范围")
    location: Optional[str] = Field(None, description="工作地点")
    tags: Optional[List[str]] = Field(None, description="职位标签")
