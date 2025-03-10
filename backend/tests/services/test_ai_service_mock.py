"""
AI服务模拟测试
"""
import pytest
from app.services.ai_service_mock import AIService

@pytest.fixture
def ai_service():
    """提供AI服务实例"""
    return AIService()

def test_parse_resume(ai_service):
    """测试解析简历内容"""
    # 准备测试数据
    ocr_content = """
    姓名：张三
    学历：本科
    技能：Python, FastAPI, Vue.js
    工作经验：3年
    联系电话：13800138000
    """
    
    # 调用方法
    result = ai_service.parse_resume(ocr_content)
    
    # 验证结果
    assert result is not None
    assert isinstance(result, dict)
    assert result.get("name") == "张三"
    assert result.get("education") == "本科"
    assert "Python" in result.get("skills", [])
    assert "FastAPI" in result.get("skills", [])
    assert "Vue.js" in result.get("skills", [])
    assert result.get("experience") == "3年"
    assert result.get("contact") == "13800138000"

def test_generate_talent_portrait(ai_service):
    """测试生成人才画像"""
    # 准备测试数据
    parsed_content = {
        "name": "李四",
        "education": "硕士",
        "skills": ["Java", "Spring Boot", "MySQL"],
        "experience": "5年"
    }
    
    # 调用方法
    result = ai_service.generate_talent_portrait(parsed_content)
    
    # 验证结果
    assert result is not None
    assert isinstance(result, str)
    assert "李四" in result
    assert "5年" in result
    assert "硕士" in result
    assert "Java" in result or "Spring Boot" in result or "MySQL" in result

def test_generate_resume_tags(ai_service):
    """测试从简历内容中提取标签"""
    # 准备测试数据
    resume_content = """
    熟练掌握Python编程语言，熟悉FastAPI框架，了解Vue.js前端开发。
    具有3年的Web开发经验，熟悉Docker容器化部署。
    """
    
    # 调用方法
    result = ai_service.generate_resume_tags(resume_content)
    
    # 验证结果
    assert result is not None
    assert isinstance(result, list)
    assert len(result) > 0
    assert "Python" in result
    assert "FastAPI" in result
    assert "Docker" in result

def test_extract_job_tags(ai_service):
    """测试从职位描述中提取标签"""
    # 准备测试数据
    job_description = """
    职位要求：
    1. 熟练掌握Java编程语言，熟悉Spring Boot框架
    2. 熟悉MySQL数据库，了解Redis缓存
    3. 具有3年以上的后端开发经验
    """
    
    # 调用方法
    result = ai_service.extract_job_tags(job_description)
    
    # 验证结果
    assert result is not None
    assert isinstance(result, list)
    assert len(result) > 0
    assert "Java" in result

def test_match_resume_to_job(ai_service):
    """测试匹配简历与职位需求"""
    # 准备测试数据
    resume_content = """
    熟练掌握Python编程语言，熟悉FastAPI框架，了解Vue.js前端开发。
    具有3年的Web开发经验，熟悉Docker容器化部署。
    """
    
    job_requirements = """
    职位要求：
    1. 熟练掌握Python编程语言，熟悉Web框架
    2. 熟悉前端开发，了解Vue.js或React
    3. 具有2年以上的Web开发经验
    """
    
    # 调用方法
    result = ai_service.match_resume_to_job(resume_content, job_requirements)
    
    # 验证结果
    assert result is not None
    assert isinstance(result, dict)
    assert "score" in result
    assert "explanation" in result
    assert result["score"] > 0
    assert isinstance(result["explanation"], str)
    assert len(result["explanation"]) > 0

def test_generate_recruitment_plan(ai_service):
    """测试生成招聘方案"""
    # 准备测试数据
    job_requirement = {
        "position_name": "Python开发工程师",
        "department": "技术部",
        "responsibilities": "负责公司产品的后端开发",
        "requirements": "熟练掌握Python编程语言，熟悉Web框架",
        "salary_range": "15k-25k",
        "location": "北京"
    }
    
    matched_resumes = [
        {
            "resume_id": 1,
            "candidate_name": "张三",
            "talent_portrait": "张三是一名有3年经验的Python开发工程师",
            "match_score": 85,
            "match_explanation": "候选人非常符合职位要求，建议安排面试"
        },
        {
            "resume_id": 2,
            "candidate_name": "李四",
            "talent_portrait": "李四是一名有2年经验的Python开发工程师",
            "match_score": 75,
            "match_explanation": "候选人基本符合职位要求，但在某些方面需要进一步提升"
        }
    ]
    
    # 调用方法
    result = ai_service.generate_recruitment_plan(job_requirement, matched_resumes)
    
    # 验证结果
    assert result is not None
    assert isinstance(result, dict)
    assert "recruitment_strategy" in result
    assert "candidate_recommendations" in result
    assert isinstance(result["recruitment_strategy"], str)
    assert isinstance(result["candidate_recommendations"], list)
    assert len(result["candidate_recommendations"]) > 0
    assert "candidate_id" in result["candidate_recommendations"][0]
    assert "recommendation_reason" in result["candidate_recommendations"][0]
