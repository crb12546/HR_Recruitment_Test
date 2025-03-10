"""
简历模型测试
"""
import pytest
from app.models.resume import Resume
from app.models.tag import Tag

def test_resume_create(db):
    """测试创建简历"""
    # 创建简历
    resume = Resume(
        candidate_name="张三",
        file_url="/uploads/resumes/test.pdf",
        file_type="application/pdf",
        ocr_content="测试简历内容",
        parsed_content="{'name': '张三', 'skills': ['Python', 'FastAPI']}",
        talent_portrait="张三是一名有3年经验的Python开发工程师"
    )
    
    # 添加到数据库
    db.add(resume)
    db.commit()
    db.refresh(resume)
    
    # 验证
    assert resume.id is not None
    assert resume.candidate_name == "张三"
    assert resume.file_url == "/uploads/resumes/test.pdf"
    assert resume.file_type == "application/pdf"
    assert resume.ocr_content == "测试简历内容"
    assert "张三" in resume.parsed_content
    assert "Python" in resume.talent_portrait
    assert resume.created_at is not None
    assert resume.updated_at is not None

def test_resume_tag_relationship(db):
    """测试简历与标签的关系"""
    # 创建标签
    tag1 = Tag(name="Python", category="skill")
    tag2 = Tag(name="FastAPI", category="skill")
    
    # 添加到数据库
    db.add(tag1)
    db.add(tag2)
    db.commit()
    
    # 创建简历
    resume = Resume(
        candidate_name="李四",
        file_url="/uploads/resumes/test2.pdf",
        file_type="application/pdf",
        ocr_content="测试简历内容",
        parsed_content="{'name': '李四', 'skills': ['Python', 'FastAPI']}",
        talent_portrait="李四是一名有2年经验的Python开发工程师"
    )
    
    # 添加标签关联
    resume.tags.append(tag1)
    resume.tags.append(tag2)
    
    # 添加到数据库
    db.add(resume)
    db.commit()
    db.refresh(resume)
    
    # 验证
    assert len(resume.tags) == 2
    assert resume.tags[0].name in ["Python", "FastAPI"]
    assert resume.tags[1].name in ["Python", "FastAPI"]
    
    # 验证反向关联
    assert len(tag1.resumes) == 1
    assert tag1.resumes[0].candidate_name == "李四"

def test_resume_to_dict(db):
    """测试简历转换为字典"""
    # 创建标签
    tag = Tag(name="Python", category="skill")
    db.add(tag)
    db.commit()
    
    # 创建简历
    resume = Resume(
        candidate_name="王五",
        file_url="/uploads/resumes/test3.pdf",
        file_type="application/pdf",
        ocr_content="测试简历内容",
        parsed_content="{'name': '王五', 'skills': ['Python']}",
        talent_portrait="王五是一名有1年经验的Python开发工程师"
    )
    
    # 添加标签关联
    resume.tags.append(tag)
    
    # 添加到数据库
    db.add(resume)
    db.commit()
    db.refresh(resume)
    
    # 转换为字典
    resume_dict = resume.to_dict()
    
    # 验证
    assert resume_dict["id"] == resume.id
    assert resume_dict["candidate_name"] == "王五"
    assert resume_dict["file_url"] == "/uploads/resumes/test3.pdf"
    assert resume_dict["file_type"] == "application/pdf"
    assert resume_dict["ocr_content"] == "测试简历内容"
    assert "王五" in resume_dict["parsed_content"]
    assert "Python" in resume_dict["talent_portrait"]
    assert resume_dict["created_at"] is not None
    assert resume_dict["updated_at"] is not None
    assert len(resume_dict["tags"]) == 1
    assert resume_dict["tags"][0]["name"] == "Python"
    assert resume_dict["tags"][0]["category"] == "skill"
