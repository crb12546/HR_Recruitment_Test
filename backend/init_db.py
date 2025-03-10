#!/usr/bin/env python
"""
数据库初始化脚本
用于创建数据库、表结构和初始数据
"""
import os
import sys
import json
import logging
from pathlib import Path

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 添加项目根目录到Python路径
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

try:
    from app.db.create_db import init_db
    from app.db.init_db import init_data
    from app.core.config import settings
except ImportError as e:
    logger.error(f"导入错误: {e}")
    logger.info("尝试直接导入...")
    sys.path.append(str(BASE_DIR / "app"))
    from db.create_db import init_db
    from db.init_db import init_data
    from core.config import settings

def load_test_data():
    """加载测试数据"""
    logger.info("加载测试数据...")
    
    test_data_dir = BASE_DIR / "test_data"
    if not test_data_dir.exists():
        logger.warning(f"测试数据目录不存在: {test_data_dir}")
        return False
    
    try:
        # 加载职位需求测试数据
        job_requirements_file = test_data_dir / "job_requirements.json"
        if job_requirements_file.exists():
            with open(job_requirements_file, "r", encoding="utf-8") as f:
                job_requirements = json.load(f)
                logger.info(f"加载了 {len(job_requirements)} 条职位需求测试数据")
        
        # 加载简历测试数据
        resumes_file = test_data_dir / "resumes.json"
        if resumes_file.exists():
            with open(resumes_file, "r", encoding="utf-8") as f:
                resumes = json.load(f)
                logger.info(f"加载了 {len(resumes)} 条简历测试数据")
        
        # 加载匹配结果测试数据
        matches_file = test_data_dir / "matches.json"
        if matches_file.exists():
            with open(matches_file, "r", encoding="utf-8") as f:
                matches = json.load(f)
                logger.info(f"加载了 {len(matches)} 条匹配结果测试数据")
        
        # 加载招聘方案测试数据
        plans_file = test_data_dir / "plans.json"
        if plans_file.exists():
            with open(plans_file, "r", encoding="utf-8") as f:
                plans = json.load(f)
                logger.info(f"加载了 {len(plans)} 条招聘方案测试数据")
        
        return True
    except Exception as e:
        logger.error(f"加载测试数据失败: {e}")
        return False

def main():
    """主函数"""
    logger.info("开始初始化数据库...")
    
    try:
        # 初始化数据库和表结构
        init_db()
        logger.info("数据库和表结构初始化成功")
        
        # 初始化基础数据
        init_data()
        logger.info("基础数据初始化成功")
        
        # 加载测试数据
        if settings.ENV == "development":
            if load_test_data():
                logger.info("测试数据加载成功")
            else:
                logger.warning("测试数据加载失败或不需要加载")
        
        logger.info("数据库初始化完成")
        return True
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
