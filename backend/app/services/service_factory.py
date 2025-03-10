"""
服务工厂模块
用于创建和获取各种服务实例
"""
import os
import logging
from app.services.ai_service import AIService
from app.services.ai_service_mock import AIService as MockAIService
from app.services.file_service import FileService
from app.services.file_service_mock import FileService as MockFileService

# 获取日志记录器
logger = logging.getLogger(__name__)

def get_ai_service():
    """获取AI服务实例"""
    # 在测试环境中使用模拟服务
    if os.getenv("MOCK_SERVICES", "False").lower() == "true" or os.getenv("ENV") == "test":
        logger.info("使用模拟AI服务")
        return MockAIService()
    logger.info("使用真实AI服务")
    return AIService()

def get_file_service():
    """获取文件服务实例"""
    # 在测试环境中使用模拟服务
    if os.getenv("MOCK_SERVICES", "False").lower() == "true" or os.getenv("ENV") == "test":
        logger.info("使用模拟文件服务")
        return MockFileService()
    logger.info("使用真实文件服务")
    return FileService()
