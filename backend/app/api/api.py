"""
API路由注册
"""
from fastapi import APIRouter
from app.api.endpoints import jobs, resumes, matches, plans, auth

api_router = APIRouter()

# 注册各模块路由
api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["招聘需求"])
api_router.include_router(resumes.router, prefix="/resumes", tags=["简历"])
api_router.include_router(matches.router, prefix="/matches", tags=["匹配"])
api_router.include_router(plans.router, prefix="/plans", tags=["招聘方案"])
