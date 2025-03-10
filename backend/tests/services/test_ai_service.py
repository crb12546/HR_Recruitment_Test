"""
AI服务测试模块
"""
import pytest
from app.services.service_factory import get_ai_service

class TestAIService:
    """AI服务测试类"""
    
    def setup_method(self):
        """测试前准备"""
        self.ai_service = get_ai_service()
    
    def test_parse_resume(self):
        """测试简历解析功能"""
        # 准备测试数据
        ocr_content = """
        姓名：张三
        学历：本科
        技能：Python, FastAPI, Vue.js
        工作经验：3年
        联系电话：13800138000
        """
        
        # 调用被测方法
        result = self.ai_service.parse_resume(ocr_content)
        
        # 验证结果
        assert isinstance(result, dict)
        assert "name" in result
        
        # 如果使用模拟服务，验证具体结果
        if hasattr(self.ai_service, "mock_data_path"):
            assert result.get("name") == "张三"
            assert result.get("education") == "本科"
            assert "Python" in result.get("skills", [])
    
    def test_generate_talent_portrait(self):
        """测试人才画像生成功能"""
        # 准备测试数据
        parsed_content = {
            "name": "张三",
            "education": "本科",
            "skills": ["Python", "FastAPI", "Vue.js"],
            "experience": "3年"
        }
        
        # 调用被测方法
        result = self.ai_service.generate_talent_portrait(parsed_content)
        
        # 验证结果
        assert isinstance(result, str)
        assert len(result) > 0
        
        # 如果使用模拟服务，验证具体结果
        if hasattr(self.ai_service, "mock_data_path"):
            assert "张三" in result
            assert "Python" in result
    
    def test_generate_resume_tags(self):
        """测试简历标签提取功能"""
        # 准备测试数据
        resume_content = """
        熟练掌握Python编程语言，熟悉FastAPI框架，有3年Web开发经验。
        精通Vue.js前端开发，了解React基础。
        熟悉Docker容器化技术，有良好的团队协作能力。
        """
        
        # 调用被测方法
        result = self.ai_service.generate_resume_tags(resume_content)
        
        # 验证结果
        assert isinstance(result, list)
        assert len(result) > 0
        
        # 如果使用模拟服务，验证具体结果
        if hasattr(self.ai_service, "mock_data_path"):
            assert "Python" in result
            assert "FastAPI" in result
    
    def test_extract_job_tags(self):
        """测试职位标签提取功能"""
        # 准备测试数据
        job_description = """
        职位要求：
        1. 熟练掌握Python编程语言，熟悉FastAPI或Flask框架
        2. 熟悉前端技术，如Vue.js或React
        3. 了解Docker容器化技术
        4. 有良好的团队协作能力
        """
        
        # 调用被测方法
        result = self.ai_service.extract_job_tags(job_description)
        
        # 验证结果
        assert isinstance(result, list)
        assert len(result) > 0
        
        # 如果使用模拟服务，验证具体结果
        if hasattr(self.ai_service, "mock_data_path"):
            assert "Python" in result
            assert "FastAPI" in result or "Flask" in result
    
    def test_match_resume_to_job(self):
        """测试简历与职位匹配功能"""
        # 准备测试数据
        resume_content = """
        熟练掌握Python编程语言，熟悉FastAPI框架，有3年Web开发经验。
        精通Vue.js前端开发，了解React基础。
        熟悉Docker容器化技术，有良好的团队协作能力。
        """
        
        job_requirements = """
        职位要求：
        1. 熟练掌握Python编程语言，熟悉FastAPI或Flask框架
        2. 熟悉前端技术，如Vue.js或React
        3. 了解Docker容器化技术
        4. 有良好的团队协作能力
        """
        
        # 调用被测方法
        result = self.ai_service.match_resume_to_job(resume_content, job_requirements)
        
        # 验证结果
        assert isinstance(result, dict)
        assert "score" in result
        assert "explanation" in result
        assert isinstance(result["score"], (int, float))
        assert 0 <= result["score"] <= 100
        assert isinstance(result["explanation"], str)
    
    def test_generate_recruitment_plan(self):
        """测试招聘方案生成功能"""
        # 准备测试数据
        job_requirement = {
            "position_name": "Python后端开发工程师",
            "department": "技术部",
            "description": "负责公司核心业务系统的开发和维护",
            "requirements": "熟练掌握Python编程语言，熟悉FastAPI或Flask框架"
        }
        
        matched_resumes = [
            {
                "resume_id": 1,
                "candidate_name": "张三",
                "match_score": 85,
                "match_explanation": "候选人技能与职位要求高度匹配"
            },
            {
                "resume_id": 2,
                "candidate_name": "李四",
                "match_score": 75,
                "match_explanation": "候选人基本符合职位要求，但经验略显不足"
            }
        ]
        
        # 调用被测方法
        result = self.ai_service.generate_recruitment_plan(job_requirement, matched_resumes)
        
        # 验证结果
        assert isinstance(result, dict)
        assert len(result) > 0
