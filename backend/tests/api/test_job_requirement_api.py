"""
招聘需求API测试
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import json
from app.core.config import settings
from app.models.job_requirement import JobRequirement

# 测试数据
test_job = {
    "position_name": "测试工程师",
    "department": "技术部",
    "responsibilities": "负责产品测试和质量保证",
    "requirements": "熟悉自动化测试，有2年以上测试经验",
    "salary_range": "10k-15k",
    "location": "北京",
    "tags": ["测试", "自动化", "质量保证"]
}

class TestJobRequirementAPI:
    """招聘需求API测试类"""
    
    def test_create_job_requirement(self, client: TestClient, db: Session, user_token_headers):
        """测试创建招聘需求"""
        response = client.post(
            f"{settings.API_V1_STR}/jobs",
            headers=user_token_headers,
            json=test_job
        )
        
        # 验证响应
        assert response.status_code == 201
        job_data = response.json()
        assert job_data["position_name"] == test_job["position_name"]
        assert job_data["department"] == test_job["department"]
        assert job_data["responsibilities"] == test_job["responsibilities"]
        assert job_data["requirements"] == test_job["requirements"]
        assert job_data["salary_range"] == test_job["salary_range"]
        assert job_data["location"] == test_job["location"]
        assert "id" in job_data
        
        # 验证数据库
        db_job = db.query(JobRequirement).filter(JobRequirement.id == job_data["id"]).first()
        assert db_job is not None
        assert db_job.position_name == test_job["position_name"]
    
    def test_read_job_requirements(self, client: TestClient, db: Session, user_token_headers):
        """测试获取招聘需求列表"""
        # 创建测试数据
        job = JobRequirement(
            position_name=test_job["position_name"],
            department=test_job["department"],
            responsibilities=test_job["responsibilities"],
            requirements=test_job["requirements"],
            salary_range=test_job["salary_range"],
            location=test_job["location"],
            tags=test_job["tags"]
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        
        # 获取列表
        response = client.get(
            f"{settings.API_V1_STR}/jobs",
            headers=user_token_headers
        )
        
        # 验证响应
        assert response.status_code == 200
        jobs = response.json()
        assert isinstance(jobs, list)
        assert len(jobs) >= 1
        
        # 验证过滤功能
        response = client.get(
            f"{settings.API_V1_STR}/jobs?position_name={test_job['position_name']}",
            headers=user_token_headers
        )
        filtered_jobs = response.json()
        assert len(filtered_jobs) >= 1
        assert any(job["position_name"] == test_job["position_name"] for job in filtered_jobs)
    
    def test_read_job_requirement(self, client: TestClient, db: Session, user_token_headers):
        """测试获取招聘需求详情"""
        # 创建测试数据
        job = JobRequirement(
            position_name=test_job["position_name"],
            department=test_job["department"],
            responsibilities=test_job["responsibilities"],
            requirements=test_job["requirements"],
            salary_range=test_job["salary_range"],
            location=test_job["location"],
            tags=test_job["tags"]
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        
        # 获取详情
        response = client.get(
            f"{settings.API_V1_STR}/jobs/{job.id}",
            headers=user_token_headers
        )
        
        # 验证响应
        assert response.status_code == 200
        job_data = response.json()
        assert job_data["id"] == job.id
        assert job_data["position_name"] == job.position_name
        assert job_data["department"] == job.department
    
    def test_update_job_requirement(self, client: TestClient, db: Session, user_token_headers):
        """测试更新招聘需求"""
        # 创建测试数据
        job = JobRequirement(
            position_name=test_job["position_name"],
            department=test_job["department"],
            responsibilities=test_job["responsibilities"],
            requirements=test_job["requirements"],
            salary_range=test_job["salary_range"],
            location=test_job["location"],
            tags=test_job["tags"]
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        
        # 更新数据
        update_data = {
            "position_name": "高级测试工程师",
            "salary_range": "15k-25k"
        }
        response = client.put(
            f"{settings.API_V1_STR}/jobs/{job.id}",
            headers=user_token_headers,
            json=update_data
        )
        
        # 验证响应
        assert response.status_code == 200
        job_data = response.json()
        assert job_data["position_name"] == update_data["position_name"]
        assert job_data["salary_range"] == update_data["salary_range"]
        assert job_data["department"] == job.department  # 未更新的字段保持不变
        
        # 验证数据库
        db_job = db.query(JobRequirement).filter(JobRequirement.id == job.id).first()
        assert db_job.position_name == update_data["position_name"]
        assert db_job.salary_range == update_data["salary_range"]
    
    def test_delete_job_requirement(self, client: TestClient, db: Session, user_token_headers):
        """测试删除招聘需求"""
        # 创建测试数据
        job = JobRequirement(
            position_name=test_job["position_name"],
            department=test_job["department"],
            responsibilities=test_job["responsibilities"],
            requirements=test_job["requirements"],
            salary_range=test_job["salary_range"],
            location=test_job["location"],
            tags=test_job["tags"]
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        
        # 删除
        response = client.delete(
            f"{settings.API_V1_STR}/jobs/{job.id}",
            headers=user_token_headers
        )
        
        # 验证响应
        assert response.status_code == 204
        
        # 验证数据库
        db_job = db.query(JobRequirement).filter(JobRequirement.id == job.id).first()
        assert db_job is None
    
    def test_parse_job_requirement(self, client: TestClient, user_token_headers):
        """测试解析招聘需求文档"""
        # 模拟文档内容
        doc_content = "职位：Python开发工程师\n部门：技术部\n工作职责：负责后端API开发\n任职要求：熟悉Python和FastAPI\n薪资：20k-30k\n地点：上海"
        
        # 创建测试文件
        import io
        file = io.BytesIO(doc_content.encode())
        file.name = "job_requirement.txt"
        
        # 发送请求
        response = client.post(
            f"{settings.API_V1_STR}/jobs/parse",
            headers=user_token_headers,
            files={"file": (file.name, file, "text/plain")}
        )
        
        # 验证响应
        assert response.status_code == 200
        parsed_data = response.json()
        assert "position_name" in parsed_data
        assert "responsibilities" in parsed_data
        assert "requirements" in parsed_data
        assert "tags" in parsed_data
    
    def test_upload_job_requirement(self, client: TestClient, db: Session, user_token_headers):
        """测试上传招聘需求文档"""
        # 模拟文档内容
        doc_content = "职位：Java开发工程师\n部门：技术部\n工作职责：负责核心系统开发\n任职要求：熟悉Java和Spring\n薪资：25k-35k\n地点：北京"
        
        # 创建测试文件
        import io
        file = io.BytesIO(doc_content.encode())
        file.name = "job_requirement.txt"
        
        # 发送请求
        response = client.post(
            f"{settings.API_V1_STR}/jobs/upload",
            headers=user_token_headers,
            files={"file": (file.name, file, "text/plain")},
            data={"position_name": "Java开发工程师", "department": "技术部"}
        )
        
        # 验证响应
        assert response.status_code == 200
        job_data = response.json()
        assert job_data["position_name"] == "Java开发工程师"
        assert job_data["department"] == "技术部"
        assert "id" in job_data
        
        # 验证数据库
        db_job = db.query(JobRequirement).filter(JobRequirement.id == job_data["id"]).first()
        assert db_job is not None
        assert db_job.position_name == "Java开发工程师"
