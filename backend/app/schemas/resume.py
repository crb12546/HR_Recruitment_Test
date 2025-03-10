"""
简历相关的Pydantic模型
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class TagBase(BaseModel):
    """标签基础模型"""
    name: str = Field(..., description="标签名称")
    category: Optional[str] = Field(None, description="标签类别")

class Tag(TagBase):
    """标签响应模型"""
    id: int
    
    class Config:
        orm_mode = True

class ResumeBase(BaseModel):
    """简历基础模型"""
    candidate_name: str = Field(..., description="候选人姓名")
    file_url: str = Field(..., description="文件URL")
    file_type: str = Field(..., description="文件类型")
    ocr_content: Optional[str] = Field(None, description="OCR识别内容")
    parsed_content: Optional[str] = Field(None, description="解析后内容")
    talent_portrait: Optional[str] = Field(None, description="人才画像")

class ResumeCreate(BaseModel):
    """创建简历模型"""
    candidate_name: Optional[str] = Field(None, description="候选人姓名")
    file_type: str = Field(..., description="文件类型")

class ResumeUpdate(BaseModel):
    """更新简历模型"""
    candidate_name: Optional[str] = Field(None, description="候选人姓名")
    ocr_content: Optional[str] = Field(None, description="OCR识别内容")
    parsed_content: Optional[str] = Field(None, description="解析后内容")
    talent_portrait: Optional[str] = Field(None, description="人才画像")

class ResumeInDB(ResumeBase):
    """数据库中的简历模型"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class Resume(ResumeInDB):
    """简历响应模型"""
    tags: List[Tag] = []
