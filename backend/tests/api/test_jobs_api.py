"""
招聘需求API测试
"""
import pytest
from fastapi.testclient import TestClient
from app.models.job_requirement import JobRequirement

def test_create_job_requirement(client, db):
    """测试创建招聘需求"""
    # 准备测试数据
    job_data = {
        "position_name": "Python开发工程师",
        "department": "技术部",
        "responsibilities": "负责公司产品的后端开发",
        "requirements": "熟练掌握Python编程语言，熟悉Web框架",
        "salary_range": "15k-25k",
        "location": "北京"
    }
    
    # 发送请求
    response = client.post("/api/v1/jobs", json=job_data)
    
    # 验证响应
    assert response.status_code == 201
    data = response.json()
    assert data["position_name"] == job_data["position_name"]
    assert data["department"] == job_data["department"]
    assert data["responsibilities"] == job_data["responsibilities"]
    assert data["requirements"] == job_data["requirements"]
    assert data["salary_range"] == job_data["salary_range"]
    assert data["location"] == job_data["location"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data
    assert "tags" in data
    
    # 验证数据库
    job = db.query(JobRequirement).filter(JobRequirement.id == data["id"]).first()
    assert job is not None
    assert job.position_name == job_data["position_name"]

def test_read_job_requirements(client, db):
    """测试获取招聘需求列表"""
    # 准备测试数据
    job1 = JobRequirement(
        position_name="Python开发工程师",
        department="技术部",
        responsibilities="负责公司产品的后端开发",
        requirements="熟练掌握Python编程语言，熟悉Web框架",
        salary_range="15k-25k",
        location="北京",
        tags=["Python", "FastAPI"]
    )
    job2 = JobRequirement(
        position_name="前端开发工程师",
        department="技术部",
        responsibilities="负责公司产品的前端开发",
        requirements="熟练掌握JavaScript，熟悉Vue.js或React",
        salary_range="15k-25k",
        location="上海",
        tags=["JavaScript", "Vue.js"]
    )
    db.add(job1)
    db.add(job2)
    db.commit()
    
    # 发送请求
    response = client.get("/api/v1/jobs")
    
    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["position_name"] in ["Python开发工程师", "前端开发工程师"]
    assert data[1]["position_name"] in ["Python开发工程师", "前端开发工程师"]
    
    # 测试过滤
    response = client.get("/api/v1/jobs?position_name=Python")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["position_name"] == "Python开发工程师"

def test_read_job_requirement(client, db):
    """测试获取招聘需求详情"""
    # 准备测试数据
    job = JobRequirement(
        position_name="Python开发工程师",
        department="技术部",
        responsibilities="负责公司产品的后端开发",
        requirements="熟练掌握Python编程语言，熟悉Web框架",
        salary_range="15k-25k",
        location="北京",
        tags=["Python", "FastAPI"]
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    
    # 发送请求
    response = client.get(f"/api/v1/jobs/{job.id}")
    
    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == job.id
    assert data["position_name"] == job.position_name
    assert data["department"] == job.department
    assert data["responsibilities"] == job.responsibilities
    assert data["requirements"] == job.requirements
    assert data["salary_range"] == job.salary_range
    assert data["location"] == job.location
    assert data["tags"] == job.tags
    
    # 测试不存在的ID
    response = client.get("/api/v1/jobs/999")
    assert response.status_code == 404

def test_update_job_requirement(client, db):
    """测试更新招聘需求"""
    # 准备测试数据
    job = JobRequirement(
        position_name="Python开发工程师",
        department="技术部",
        responsibilities="负责公司产品的后端开发",
        requirements="熟练掌握Python编程语言，熟悉Web框架",
        salary_range="15k-25k",
        location="北京",
        tags=["Python", "FastAPI"]
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    
    # 准备更新数据
    update_data = {
        "position_name": "高级Python开发工程师",
        "salary_range": "20k-30k"
    }
    
    # 发送请求
    response = client.put(f"/api/v1/jobs/{job.id}", json=update_data)
    
    # 验证响应
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == job.id
    assert data["position_name"] == update_data["position_name"]
    assert data["salary_range"] == update_data["salary_range"]
    assert data["department"] == job.department  # 未更新的字段保持不变
    
    # 验证数据库
    updated_job = db.query(JobRequirement).filter(JobRequirement.id == job.id).first()
    assert updated_job.position_name == update_data["position_name"]
    assert updated_job.salary_range == update_data["salary_range"]
    
    # 测试不存在的ID
    response = client.put("/api/v1/jobs/999", json=update_data)
    assert response.status_code == 404

def test_delete_job_requirement(client, db):
    """测试删除招聘需求"""
    # 准备测试数据
    job = JobRequirement(
        position_name="Python开发工程师",
        department="技术部",
        responsibilities="负责公司产品的后端开发",
        requirements="熟练掌握Python编程语言，熟悉Web框架",
        salary_range="15k-25k",
        location="北京",
        tags=["Python", "FastAPI"]
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    
    # 发送请求
    response = client.delete(f"/api/v1/jobs/{job.id}")
    
    # 验证响应
    assert response.status_code == 204
    
    # 验证数据库
    deleted_job = db.query(JobRequirement).filter(JobRequirement.id == job.id).first()
    assert deleted_job is None
    
    # 测试不存在的ID
    response = client.delete("/api/v1/jobs/999")
    assert response.status_code == 404
