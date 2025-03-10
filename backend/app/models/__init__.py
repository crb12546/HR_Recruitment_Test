"""
模型包初始化
"""
# 导入基类
from app.db.base import Base

# 导入所有模型以确保它们在创建表时被注册
from .job_requirement import JobRequirement
from .resume import Resume
from .match import Match
from .plan import Plan
from .user import User
from .tag import Tag

__all__ = ['Base', 'JobRequirement', 'Resume', 'Match', 'Plan', 'User', 'Tag']
