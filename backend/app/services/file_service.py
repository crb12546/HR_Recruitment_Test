"""
文件服务模块
提供文件上传、下载和管理功能
"""
import os
import logging
import base64
from typing import Dict, Any, Optional
from fastapi import UploadFile
from app.core.config import settings

# 获取日志记录器
logger = logging.getLogger(__name__)

class FileService:
    """文件服务类，提供文件上传、下载和管理功能"""
    
    def __init__(self):
        """初始化文件服务"""
        self.storage_path = os.getenv("STORAGE_PATH", "./uploads")
        
        # 确保存储目录存在
        os.makedirs(self.storage_path, exist_ok=True)
        logger.info(f"文件服务初始化成功，存储路径: {self.storage_path}")
    
    async def upload_file(self, file: UploadFile, folder: str = "resumes") -> Dict[str, Any]:
        """上传文件"""
        logger.info(f"开始上传文件: {file.filename}, 文件类型: {file.content_type}")
        
        try:
            # 确保目标文件夹存在
            folder_path = os.path.join(self.storage_path, folder)
            os.makedirs(folder_path, exist_ok=True)
            
            # 读取文件内容
            file_content = await file.read()
            
            # 生成文件名
            import uuid
            import time
            file_ext = os.path.splitext(file.filename)[1]
            file_name = f"{int(time.time())}_{uuid.uuid4().hex}{file_ext}"
            file_path = os.path.join(folder_path, file_name)
            
            # 保存文件
            with open(file_path, "wb") as f:
                f.write(file_content)
            
            # 生成文件URL
            file_url = f"/uploads/{folder}/{file_name}"
            
            logger.info(f"文件上传成功: {file_path}")
            return {
                "file_name": file_name,
                "file_path": file_path,
                "file_url": file_url,
                "file_type": file.content_type,
                "file_size": len(file_content)
            }
            
        except Exception as e:
            logger.error(f"文件上传失败: {str(e)}")
            raise e
    
    def get_file_content(self, file_path: str) -> bytes:
        """获取文件内容"""
        logger.info(f"开始获取文件内容: {file_path}")
        
        try:
            # 如果是相对路径，转换为绝对路径
            if not os.path.isabs(file_path):
                file_path = os.path.join(self.storage_path, file_path)
            
            # 读取文件内容
            with open(file_path, "rb") as f:
                file_content = f.read()
            
            logger.info(f"文件内容获取成功: {file_path}")
            return file_content
            
        except Exception as e:
            logger.error(f"文件内容获取失败: {str(e)}")
            raise e
    
    def get_file_as_base64(self, file_path: str) -> str:
        """获取文件内容并转换为Base64编码"""
        logger.info(f"开始获取文件内容并转换为Base64: {file_path}")
        
        try:
            # 获取文件内容
            file_content = self.get_file_content(file_path)
            
            # 转换为Base64编码
            base64_content = base64.b64encode(file_content).decode("utf-8")
            
            logger.info(f"文件内容转换为Base64成功: {file_path}")
            return base64_content
            
        except Exception as e:
            logger.error(f"文件内容转换为Base64失败: {str(e)}")
            raise e
    
    def delete_file(self, file_path: str) -> bool:
        """删除文件"""
        logger.info(f"开始删除文件: {file_path}")
        
        try:
            # 如果是相对路径，转换为绝对路径
            if not os.path.isabs(file_path):
                file_path = os.path.join(self.storage_path, file_path)
            
            # 检查文件是否存在
            if not os.path.exists(file_path):
                logger.warning(f"文件不存在，无法删除: {file_path}")
                return False
            
            # 删除文件
            os.remove(file_path)
            
            logger.info(f"文件删除成功: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"文件删除失败: {str(e)}")
            return False
