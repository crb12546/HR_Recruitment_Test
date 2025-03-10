"""
AI服务模块
提供基于GPT-4O的智能分析功能
"""
import os
import json
import logging
from typing import Dict, Any, List, Optional
from openai import OpenAI
from app.core.config import settings

# 获取日志记录器
logger = logging.getLogger(__name__)

class AIService:
    """AI服务类，提供基于GPT-4O的智能分析功能"""
    
    def __init__(self):
        """初始化AI服务"""
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.GPT_MODEL
        
        # 初始化OpenAI客户端
        try:
            self.client = OpenAI(api_key=self.api_key)
            logger.info(f"AI服务初始化成功，使用模型: {self.model}")
        except Exception as e:
            logger.error(f"AI服务初始化失败: {str(e)}")
            self.client = None
    
    def parse_resume(self, ocr_content: str) -> Dict[str, Any]:
        """解析简历内容"""
        logger.info("开始解析简历内容")
        
        # 如果OCR内容为空，返回空结果
        if not ocr_content:
            logger.warning("OCR内容为空，无法解析简历")
            return {}
        
        try:
            # 构建提示词
            prompt = f"""
            请解析以下简历内容，提取关键信息，并以JSON格式返回。
            需要提取的字段包括：
            - name: 姓名
            - education: 学历
            - skills: 技能列表
            - experience: 工作经验
            - contact: 联系方式
            
            简历内容：
            {ocr_content}
            """
            
            # 调用GPT-4O API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位专业的HR招聘助手，擅长解析简历内容。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000,
                response_format={"type": "json_object"}
            )
            
            # 解析JSON响应
            content = response.choices[0].message.content
            parsed_content = json.loads(content)
            
            logger.info(f"简历解析成功: {parsed_content.get('name', '未知')}")
            return parsed_content
            
        except Exception as e:
            logger.error(f"简历解析失败: {str(e)}")
            return {}
    
    def generate_talent_portrait(self, parsed_content: Dict[str, Any]) -> str:
        """生成人才画像"""
        logger.info("开始生成人才画像")
        
        # 如果解析内容为空，返回空结果
        if not parsed_content:
            logger.warning("解析内容为空，无法生成人才画像")
            return ""
        
        try:
            # 构建提示词
            prompt = f"""
            请根据以下候选人信息，生成一段专业的人才画像，不超过200字。
            
            候选人信息：
            {json.dumps(parsed_content, ensure_ascii=False, indent=2)}
            """
            
            # 调用GPT-4O API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位专业的HR招聘助手，擅长撰写人才画像。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=300
            )
            
            # 获取响应内容
            talent_portrait = response.choices[0].message.content.strip()
            
            logger.info(f"人才画像生成成功: {talent_portrait[:50]}...")
            return talent_portrait
            
        except Exception as e:
            logger.error(f"人才画像生成失败: {str(e)}")
            return ""
    
    def generate_resume_tags(self, resume_content: str) -> List[str]:
        """从简历内容中提取标签"""
        logger.info("开始从简历内容中提取标签")
        
        # 如果简历内容为空，返回空列表
        if not resume_content:
            logger.warning("简历内容为空，无法提取标签")
            return []
        
        try:
            # 构建提示词
            prompt = f"""
            请从以下简历内容中提取关键技能标签，返回一个JSON数组。
            标签应该包括技术技能、行业经验、教育背景等关键词。
            最多返回10个标签。
            
            简历内容：
            {resume_content}
            """
            
            # 调用GPT-4O API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位专业的HR招聘助手，擅长从简历中提取关键技能标签。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=200,
                response_format={"type": "json_object"}
            )
            
            # 解析JSON响应
            content = response.choices[0].message.content
            result = json.loads(content)
            tags = result.get("tags", [])
            
            logger.info(f"标签提取成功: {tags}")
            return tags
            
        except Exception as e:
            logger.error(f"标签提取失败: {str(e)}")
            return []
    
    def extract_job_tags(self, job_description: str) -> List[str]:
        """从职位描述中提取标签"""
        logger.info("开始从职位描述中提取标签")
        
        # 如果职位描述为空，返回空列表
        if not job_description:
            logger.warning("职位描述为空，无法提取标签")
            return []
        
        try:
            # 构建提示词
            prompt = f"""
            请从以下职位描述中提取关键技能标签，返回一个JSON数组。
            标签应该包括技术要求、行业经验、教育背景等关键词。
            最多返回10个标签。
            
            职位描述：
            {job_description}
            """
            
            # 调用GPT-4O API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位专业的HR招聘助手，擅长从职位描述中提取关键技能标签。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=200,
                response_format={"type": "json_object"}
            )
            
            # 解析JSON响应
            content = response.choices[0].message.content
            result = json.loads(content)
            tags = result.get("tags", [])
            
            logger.info(f"标签提取成功: {tags}")
            return tags
            
        except Exception as e:
            logger.error(f"标签提取失败: {str(e)}")
            return []
    
    def match_resume_to_job(self, resume_content: str, job_requirements: str) -> Dict[str, Any]:
        """匹配简历与职位需求"""
        logger.info("开始匹配简历与职位需求")
        
        # 如果简历内容或职位需求为空，返回空结果
        if not resume_content or not job_requirements:
            logger.warning("简历内容或职位需求为空，无法进行匹配")
            return {
                "score": 0,
                "explanation": "无法进行匹配，缺少必要信息"
            }
        
        try:
            # 构建提示词
            prompt = f"""
            请根据以下职位要求和候选人简历，评估候选人与职位的匹配度。
            要求：
            1. 返回0-100的匹配分数
            2. 提供匹配理由，不超过100字
            3. 以JSON格式返回，如{{"score": 85, "explanation": "匹配理由"}}
            
            职位要求：
            {job_requirements}
            
            候选人简历：
            {resume_content}
            """
            
            # 调用GPT-4O API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位专业的HR招聘助手，擅长评估候选人与职位的匹配度。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=200,
                response_format={"type": "json_object"}
            )
            
            # 解析JSON响应
            content = response.choices[0].message.content
            result = json.loads(content)
            
            logger.info(f"匹配评估成功: 分数={result.get('score', 0)}")
            return {
                "score": result.get("score", 0),
                "explanation": result.get("explanation", "无匹配理由")
            }
            
        except Exception as e:
            logger.error(f"匹配评估失败: {str(e)}")
            return {
                "score": 0,
                "explanation": f"匹配评估失败: {str(e)}"
            }
    
    def generate_recruitment_plan(self, job_requirement: Dict[str, Any], matched_resumes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """生成招聘方案"""
        logger.info("开始生成招聘方案")
        
        # 如果职位需求或匹配简历为空，返回空结果
        if not job_requirement or not matched_resumes:
            logger.warning("职位需求或匹配简历为空，无法生成招聘方案")
            return {}
        
        try:
            # 构建提示词
            prompt = f"""
            请根据以下职位需求和候选人匹配结果，生成一份招聘方案。
            方案应包括：
            1. 招聘策略
            2. 候选人推荐理由
            3. 面试建议
            
            职位需求：
            {json.dumps(job_requirement, ensure_ascii=False, indent=2)}
            
            候选人匹配结果（按匹配度排序）：
            {json.dumps(matched_resumes, ensure_ascii=False, indent=2)}
            """
            
            # 调用GPT-4O API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位专业的HR招聘助手，擅长制定招聘方案。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=1000,
                response_format={"type": "json_object"}
            )
            
            # 解析JSON响应
            content = response.choices[0].message.content
            plan = json.loads(content)
            
            logger.info("招聘方案生成成功")
            return plan
            
        except Exception as e:
            logger.error(f"招聘方案生成失败: {str(e)}")
            return {}
