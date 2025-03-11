"""
AI服务模拟模块
提供AI服务的模拟实现，用于测试和开发环境
"""
import os
import json
import logging
from typing import Dict, Any, List, Optional

# 获取日志记录器
logger = logging.getLogger(__name__)

class AIService:
    """AI服务模拟类，提供模拟的智能分析功能"""
    
    def __init__(self):
        """初始化AI服务模拟类"""
        self.mock_data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                          "tests", "mocks", "data")
        logger.info(f"初始化模拟AI服务，数据路径: {self.mock_data_path}")
    
    def parse_resume(self, ocr_content: str) -> Dict[str, Any]:
        """解析简历内容（模拟实现）"""
        logger.info("模拟解析简历内容")
        
        # 如果OCR内容为空，返回空结果
        if not ocr_content:
            return {}
        
        # 简单解析OCR内容
        parsed_content = {}
        lines = ocr_content.split("\n")
        
        for line in lines:
            line = line.strip()
            if "：" in line:
                key, value = line.split("：", 1)
                key = key.strip()
                value = value.strip()
                if key == "姓名":
                    parsed_content["name"] = value
                elif key == "学历":
                    parsed_content["education"] = value
                elif key == "技能":
                    parsed_content["skills"] = [skill.strip() for skill in value.split(",")]
                elif key == "工作经验":
                    parsed_content["experience"] = value
                elif key == "联系电话":
                    parsed_content["contact"] = value
        
        return parsed_content
    
    def generate_talent_portrait(self, parsed_content: Dict[str, Any]) -> str:
        """生成人才画像（模拟实现）"""
        logger.info("模拟生成人才画像")
        
        # 如果解析内容为空，返回空结果
        if not parsed_content:
            return ""
        
        # 根据解析内容生成人才画像
        name = parsed_content.get("name", "候选人")
        education = parsed_content.get("education", "")
        skills = parsed_content.get("skills", [])
        experience = parsed_content.get("experience", "")
        
        skills_str = "、".join(skills) if skills else "相关技能"
        
        return f"{name}是一名有{experience}经验的开发工程师，{education}学历，精通{skills_str}。"
    
    def generate_resume_tags(self, resume_content: str) -> List[str]:
        """从简历内容中提取标签（模拟实现）"""
        logger.info("模拟从简历内容中提取标签")
        
        # 如果简历内容为空，返回空列表
        if not resume_content:
            return []
        
        # 模拟标签提取
        default_tags = ["Python", "Java", "SQL", "FastAPI", "Vue.js", "React", "Docker", "Kubernetes"]
        
        # 根据简历内容选择相关标签
        selected_tags = []
        for tag in default_tags:
            if tag.lower() in resume_content.lower():
                selected_tags.append(tag)
        
        # 确保至少有一些标签
        if len(selected_tags) < 3:
            for tag in default_tags:
                if tag not in selected_tags:
                    selected_tags.append(tag)
                    if len(selected_tags) >= 5:
                        break
        
        return selected_tags
    
    def extract_job_tags(self, job_description: str) -> List[str]:
        """从职位描述中提取标签（模拟实现）"""
        logger.info("模拟从职位描述中提取标签")
        
        # 如果职位描述为空，返回空列表
        if not job_description:
            return []
        
        # 模拟标签提取
        default_tags = ["Python", "Java", "SQL", "FastAPI", "Vue.js", "React", "Docker", "Kubernetes"]
        
        # 根据职位描述选择相关标签
        selected_tags = []
        for tag in default_tags:
            if tag.lower() in job_description.lower() or len(selected_tags) < 3:
                selected_tags.append(tag)
                if len(selected_tags) >= 5:  # 最多返回5个标签
                    break
        
        return selected_tags
    
    def match_resume_to_job(self, resume_content: str, job_requirements: str) -> Dict[str, Any]:
        """匹配简历与职位需求（模拟实现）"""
        logger.info("模拟匹配简历与职位需求")
        
        # 如果简历内容或职位需求为空，返回空结果
        if not resume_content or not job_requirements:
            return {
                "score": 0,
                "explanation": "无法进行匹配，缺少必要信息"
            }
        
        # 简单匹配分析
        result = {
            "score": 75,
            "explanation": "候选人基本符合职位要求，但在某些方面需要进一步提升"
        }
        
        # 根据内容调整匹配结果
        if len(resume_content) > 500 and len(job_requirements) > 200:
            result["score"] = 85
            result["explanation"] = "候选人非常符合职位要求，建议安排面试"
        
        return result
    
    def generate_recruitment_plan(self, job_requirement: Dict[str, Any], matched_resumes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """生成招聘方案（模拟实现）"""
        logger.info("模拟生成招聘方案")
        
        # 如果职位需求或匹配简历为空，返回空结果
        if not job_requirement or not matched_resumes:
            return {}
        
        # 模拟招聘方案
        plan = {
            "recruitment_strategy": "建议采用多渠道招聘策略，包括内部推荐、社交媒体和招聘网站。",
            "candidate_recommendations": [
                {
                    "candidate_id": matched_resume.get("resume_id", 0),
                    "recommendation_reason": f"匹配度{matched_resume.get('match_score', 0)}分，{matched_resume.get('match_explanation', '')}"
                } for matched_resume in matched_resumes[:3]  # 最多推荐3名候选人
            ],
            "interview_suggestions": "建议采用两轮面试流程，第一轮技术面试，第二轮团队文化匹配面试。"
        }
        
        return plan
