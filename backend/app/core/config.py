"""
应用配置
"""
import os
from typing import List
from pydantic import BaseSettings

class Settings(BaseSettings):
    """应用配置类"""
    # 项目信息
    PROJECT_NAME: str = "HR招聘系统"
    PROJECT_DESCRIPTION: str = "AI智能招聘系统API服务"
    PROJECT_VERSION: str = "0.1.0"
    
    # API配置
    API_V1_STR: str = "/api/v1"
    
    # 安全配置
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8天
    
    # 数据库配置
    # 开发环境使用SQLite，生产环境使用MySQL
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "sqlite:///./hr_recruitment.db"
    )
    
    # CORS配置
    CORS_ORIGINS: List[str] = [
        "http://localhost:8080",
        "http://localhost:3000",
        "http://localhost",
    ]
    
    # GPT配置
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GPT_MODEL: str = "gpt-4o"
    
    # 环境配置
    ENV: str = os.getenv("ENV", "development")
    
    class Config:
        env_file = ".env"

# 创建设置实例
settings = Settings()
