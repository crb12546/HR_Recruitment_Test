"""
文件服务模拟模块
提供文件服务的模拟实现，用于测试和开发环境
"""
import os
import logging
import base64
from typing import Dict, Any, Optional
from fastapi import UploadFile

# 获取日志记录器
logger = logging.getLogger(__name__)

class FileService:
    """文件服务模拟类，提供模拟的文件上传、下载和管理功能"""
    
    def __init__(self):
        """初始化文件服务模拟类"""
        self.storage_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                         "tests", "mocks", "uploads")
        
        # 确保存储目录存在
        os.makedirs(self.storage_path, exist_ok=True)
        logger.info(f"初始化模拟文件服务，存储路径: {self.storage_path}")
    
    async def upload_file(self, file: UploadFile, folder: str = "resumes") -> Dict[str, Any]:
        """上传文件（模拟实现）"""
        logger.info(f"模拟上传文件: {file.filename}, 文件类型: {file.content_type}")
        
        try:
            # 生成文件名
            import uuid
            import time
            file_ext = os.path.splitext(file.filename)[1]
            file_name = f"{int(time.time())}_{uuid.uuid4().hex}{file_ext}"
            
            # 生成文件URL
            file_url = f"/uploads/{folder}/{file_name}"
            
            logger.info(f"模拟文件上传成功: {file_url}")
            return {
                "file_name": file_name,
                "file_path": f"{self.storage_path}/{folder}/{file_name}",
                "file_url": file_url,
                "file_type": file.content_type,
                "file_size": 1024  # 模拟文件大小
            }
            
        except Exception as e:
            logger.error(f"模拟文件上传失败: {str(e)}")
            raise e
    
    def get_file_content(self, file_path: str) -> bytes:
        """获取文件内容（模拟实现）"""
        logger.info(f"模拟获取文件内容: {file_path}")
        
        # 返回模拟文件内容
        return b"This is a mock file content."
    
    def get_file_as_base64(self, file_path: str) -> str:
        """获取文件内容并转换为Base64编码（模拟实现）"""
        logger.info(f"模拟获取文件内容并转换为Base64: {file_path}")
        
        # 返回模拟Base64编码
        return base64.b64encode(b"This is a mock file content.").decode("utf-8")
    
    def delete_file(self, file_path: str) -> bool:
        """删除文件（模拟实现）"""
        logger.info(f"模拟删除文件: {file_path}")
        
        # 返回模拟删除结果
        return True
