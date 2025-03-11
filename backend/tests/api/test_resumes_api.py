"""
简历API测试模块
"""
import pytest
from fastapi.testclient import TestClient
from app.models.resume import Resume

def test_create_resume(client, db):
    """测试创建简历"""
    # 准备测试数据
    resume_data = {
        "candidate_name": "张三",
        "file_url": "/uploads/resumes/test.pdf",
        "file_type": "application/pdf",
        "ocr_content": "测试简历内容",
        "parsed_content": "{'name': '张三', 'skills': ['Python', 'FastAPI']}",
        "talent_portrait": "张三是一名有3年经验的Python开发工程师"
    }
    
    # 发送请求
    response = client.post("/api/v1/resumes", json=resume_data)
    
    # 验证响应
    assert response.status_code == 201
    data = response.json()
    assert data["candidate_name"] == resume_data["candidate_name"]
    assert data["file_url"] == resume_data["file_url"]
    assert data["file_type"] == resume_data["file_type"]
    assert data["ocr_content"] == resume_data["ocr_content"]
    assert data["parsed_content"] == resume_data["parsed_content"]
    assert data["talent_portrait"] == resume_data["talent_portrait"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data
    
    # 验证数据库
    resume = db.query(Resume).filter(Resume.id == data["id"]).first()
    assert resume is not None
    assert resume.candidate_name == resume_data["candidate_name"]

def test_read_resumes(client, db):
    """测试获取简历列表"""
    # 准备测试数据
    resume1 = Resume(
        candidate_name="张三",
        file_url="/uploads/resumes/test1.pdf",
        file_type="application/pdf",
        ocr_content="测试简历内容1",
        parsed_content="{'name': '张三', 'skills': ['Python', 'FastAPI']}",
        talent_portrait="张三是一名有3年经验的Python开发工程师"
    )
    resume2 = Resume(
        candidate_name="李四",
        file_url="/uploads/resumes/test2.pdf",
        file_type="application/pdf",
        ocr_content="测试简历内容2",
        parsed_content="{'name': '李四', 'skills': ['JavaScript', 'Vue.js']}",
        talent_portrait="李四是一名有2年经验的前端开发工程师"
    )
    db.add(resume1)
    db.add(resume2)
    db.commit()
    
    # 发送请求
    response = client.get("/api/v1/resumes")
    
    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["candidate_name"] in ["张三", "李四"]
    assert data[1]["candidate_name"] in ["张三", "李四"]
    
    # 测试过滤
    response = client.get("/api/v1/resumes?candidate_name=张三")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["candidate_name"] == "张三"

def test_read_resume(client, db):
    """测试获取简历详情"""
    # 准备测试数据
    resume = Resume(
        candidate_name="王五",
        file_url="/uploads/resumes/test3.pdf",
        file_type="application/pdf",
        ocr_content="测试简历内容3",
        parsed_content="{'name': '王五', 'skills': ['Java', 'Spring']}",
        talent_portrait="王五是一名有5年经验的Java开发工程师"
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    
    # 发送请求
    response = client.get(f"/api/v1/resumes/{resume.id}")
    
    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == resume.id
    assert data["candidate_name"] == resume.candidate_name
    assert data["file_url"] == resume.file_url
    assert data["file_type"] == resume.file_type
    assert data["ocr_content"] == resume.ocr_content
    assert data["parsed_content"] == resume.parsed_content
    assert data["talent_portrait"] == resume.talent_portrait
    
    # 测试不存在的ID
    response = client.get("/api/v1/resumes/999")
    assert response.status_code == 404

def test_update_resume(client, db):
    """测试更新简历"""
    # 准备测试数据
    resume = Resume(
        candidate_name="赵六",
        file_url="/uploads/resumes/test4.pdf",
        file_type="application/pdf",
        ocr_content="测试简历内容4",
        parsed_content="{'name': '赵六', 'skills': ['Python', 'Django']}",
        talent_portrait="赵六是一名有4年经验的Python开发工程师"
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    
    # 准备更新数据
    update_data = {
        "candidate_name": "赵六(更新)",
        "talent_portrait": "赵六是一名有4年经验的全栈开发工程师"
    }
    
    # 发送请求
    response = client.put(f"/api/v1/resumes/{resume.id}", json=update_data)
    
    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == resume.id
    assert data["candidate_name"] == update_data["candidate_name"]
    assert data["talent_portrait"] == update_data["talent_portrait"]
    assert data["file_url"] == resume.file_url  # 未更新的字段保持不变
    
    # 验证数据库
    updated_resume = db.query(Resume).filter(Resume.id == resume.id).first()
    assert updated_resume.candidate_name == update_data["candidate_name"]
    assert updated_resume.talent_portrait == update_data["talent_portrait"]
    
    # 测试不存在的ID
    response = client.put("/api/v1/resumes/999", json=update_data)
    assert response.status_code == 404

def test_delete_resume(client, db):
    """测试删除简历"""
    # 准备测试数据
    resume = Resume(
        candidate_name="孙七",
        file_url="/uploads/resumes/test5.pdf",
        file_type="application/pdf",
        ocr_content="测试简历内容5",
        parsed_content="{'name': '孙七', 'skills': ['C++', 'Qt']}",
        talent_portrait="孙七是一名有6年经验的C++开发工程师"
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    
    # 发送请求
    response = client.delete(f"/api/v1/resumes/{resume.id}")
    
    # 验证响应
    assert response.status_code == 204
    
    # 验证数据库
    deleted_resume = db.query(Resume).filter(Resume.id == resume.id).first()
    assert deleted_resume is None
    
    # 测试不存在的ID
    response = client.delete("/api/v1/resumes/999")
    assert response.status_code == 404
