"""
招聘需求API端点
"""
from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Body
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging
import json
from app.db.session import get_db
from app.models.job_requirement import JobRequirement
from app.schemas.job import Job, JobCreate, JobUpdate, JobParseResult
from app.services.service_factory import get_ai_service, get_file_service
from app.utils.db_utils import safe_commit

# 获取日志记录器
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/parse", response_model=JobParseResult)
async def parse_job_requirement_document(
    *,
    file: UploadFile = File(...)
) -> Any:
    """
    解析招聘需求文档（不保存到数据库）
    """
    try:
        # 记录请求数据
        logger.info(f"解析招聘需求文档请求: 文件名={file.filename}")
        
        # 读取文件内容
        content = await file.read()
        content_str = content.decode("utf-8", errors="ignore")
        
        # 初始化AI服务
        ai_service = get_ai_service()
        
        # 解析文档内容
        parsed_content = ai_service.parse_job_requirement(content_str)
        
        # 提取职位标签
        job_description = f"{parsed_content.get('position_name', '')}\n{parsed_content.get('responsibilities', '')}\n{parsed_content.get('requirements', '')}"
        tags = ai_service.extract_job_tags(job_description)
        
        # 添加标签到解析结果
        parsed_content["tags"] = tags
        
        # 记录成功解析
        logger.info(f"成功解析招聘需求文档: 职位={parsed_content.get('position_name', '未知')}")
        
        return parsed_content
        
    except Exception as e:
        logger.error(f"解析招聘需求文档失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"解析招聘需求文档失败: {str(e)}"
        )

@router.post("", response_model=Job, status_code=status.HTTP_201_CREATED)
def create_job_requirement(
    *,
    db: Session = Depends(get_db),
    job_in: JobCreate
) -> Any:
    """
    创建招聘需求
    """
    try:
        # 记录请求数据
        logger.info(f"创建招聘需求请求: {job_in.dict()}")
        
        # 初始化AI服务
        ai_service = get_ai_service()
        
        # 提取职位标签
        job_description = f"{job_in.position_name}\n{job_in.responsibilities}\n{job_in.requirements}"
        tags = ai_service.extract_job_tags(job_description)
        
        # 创建招聘需求
        job = JobRequirement(
            position_name=job_in.position_name,
            department=job_in.department,
            responsibilities=job_in.responsibilities,
            requirements=job_in.requirements,
            salary_range=job_in.salary_range,
            location=job_in.location,
            tags=tags
        )
        
        # 保存到数据库
        db.add(job)
        if not safe_commit(db, "创建招聘需求失败"):
            raise HTTPException(status_code=500, detail="数据库保存失败")
        
        db.refresh(job)
        
        # 记录成功创建
        logger.info(f"成功创建招聘需求: ID={job.id}, 职位={job.position_name}")
        
        return job
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"数据库错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据库操作失败: {str(e)}"
        )
    except Exception as e:
        logger.error(f"创建招聘需求失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建招聘需求失败: {str(e)}"
        )

@router.get("", response_model=List[Job])
def read_job_requirements(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    position_name: Optional[str] = None,
    department: Optional[str] = None
) -> Any:
    """
    获取招聘需求列表
    """
    try:
        # 构建查询
        query = db.query(JobRequirement)
        
        # 应用过滤条件
        if position_name:
            query = query.filter(JobRequirement.position_name.ilike(f"%{position_name}%"))
        if department:
            query = query.filter(JobRequirement.department == department)
        
        # 应用分页
        jobs = query.order_by(JobRequirement.created_at.desc()).offset(skip).limit(limit).all()
        
        return jobs
        
    except SQLAlchemyError as e:
        logger.error(f"数据库错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据库操作失败: {str(e)}"
        )
    except Exception as e:
        logger.error(f"获取招聘需求列表失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取招聘需求列表失败: {str(e)}"
        )

@router.get("/{job_id}", response_model=Job)
def read_job_requirement(
    *,
    db: Session = Depends(get_db),
    job_id: int
) -> Any:
    """
    获取招聘需求详情
    """
    try:
        # 查询招聘需求
        job = db.query(JobRequirement).filter(JobRequirement.id == job_id).first()
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"招聘需求不存在: ID={job_id}"
            )
        
        return job
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"数据库错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据库操作失败: {str(e)}"
        )
    except Exception as e:
        logger.error(f"获取招聘需求详情失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取招聘需求详情失败: {str(e)}"
        )

@router.put("/{job_id}", response_model=Job)
def update_job_requirement(
    *,
    db: Session = Depends(get_db),
    job_id: int,
    job_in: JobUpdate
) -> Any:
    """
    更新招聘需求
    """
    try:
        # 查询招聘需求
        job = db.query(JobRequirement).filter(JobRequirement.id == job_id).first()
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"招聘需求不存在: ID={job_id}"
            )
        
        # 更新字段
        update_data = job_in.dict(exclude_unset=True)
        
        # 如果更新了职位描述相关字段，重新提取标签
        if any(field in update_data for field in ["position_name", "responsibilities", "requirements"]):
            # 初始化AI服务
            ai_service = get_ai_service()
            
            # 提取职位标签
            position_name = update_data.get("position_name", job.position_name)
            responsibilities = update_data.get("responsibilities", job.responsibilities)
            requirements = update_data.get("requirements", job.requirements)
            job_description = f"{position_name}\n{responsibilities}\n{requirements}"
            tags = ai_service.extract_job_tags(job_description)
            
            # 更新标签
            update_data["tags"] = tags
        
        # 应用更新
        for field, value in update_data.items():
            setattr(job, field, value)
        
        # 保存到数据库
        if not safe_commit(db, f"更新招聘需求失败: ID={job_id}"):
            raise HTTPException(status_code=500, detail="数据库保存失败")
        
        db.refresh(job)
        
        # 记录成功更新
        logger.info(f"成功更新招聘需求: ID={job.id}, 职位={job.position_name}")
        
        return job
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"数据库错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据库操作失败: {str(e)}"
        )
    except Exception as e:
        logger.error(f"更新招聘需求失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新招聘需求失败: {str(e)}"
        )

@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job_requirement(
    *,
    db: Session = Depends(get_db),
    job_id: int
):
    """
    删除招聘需求
    """
    try:
        # 查询招聘需求
        job = db.query(JobRequirement).filter(JobRequirement.id == job_id).first()
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"招聘需求不存在: ID={job_id}"
            )
        
        # 删除招聘需求
        db.delete(job)
        if not safe_commit(db, f"删除招聘需求失败: ID={job_id}"):
            raise HTTPException(status_code=500, detail="数据库操作失败")
        
        # 记录成功删除
        logger.info(f"成功删除招聘需求: ID={job_id}")
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"数据库错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据库操作失败: {str(e)}"
        )
    except Exception as e:
        logger.error(f"删除招聘需求失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除招聘需求失败: {str(e)}"
        )

@router.post("/upload", response_model=Job)
async def upload_job_requirement(
    *,
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
    position_name: Optional[str] = Form(None),
    department: Optional[str] = Form(None)
) -> Any:
    """
    上传并解析招聘需求文档
    """
    try:
        # 记录请求数据
        logger.info(f"上传招聘需求文档请求: 文件名={file.filename}, 职位={position_name}, 部门={department}")
        
        # 读取文件内容
        content = await file.read()
        content_str = content.decode("utf-8", errors="ignore")
        
        # 初始化AI服务
        ai_service = get_ai_service()
        
        # 解析文档内容
        parsed_content = ai_service.parse_job_requirement(content_str)
        
        # 提取职位标签
        job_description = f"{parsed_content.get('position_name', '')}\n{parsed_content.get('responsibilities', '')}\n{parsed_content.get('requirements', '')}"
        tags = ai_service.extract_job_tags(job_description)
        
        # 使用解析结果或表单提供的值
        job_position_name = position_name or parsed_content.get("position_name", "未命名职位")
        job_department = department or parsed_content.get("department", "")
        
        # 创建招聘需求
        job = JobRequirement(
            position_name=job_position_name,
            department=job_department,
            responsibilities=parsed_content.get("responsibilities", ""),
            requirements=parsed_content.get("requirements", ""),
            salary_range=parsed_content.get("salary_range", ""),
            location=parsed_content.get("location", ""),
            tags=tags
        )
        
        # 保存到数据库
        db.add(job)
        if not safe_commit(db, "创建招聘需求失败"):
            raise HTTPException(status_code=500, detail="数据库保存失败")
        
        db.refresh(job)
        
        # 记录成功创建
        logger.info(f"成功创建招聘需求: ID={job.id}, 职位={job.position_name}")
        
        return job
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"数据库错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据库操作失败: {str(e)}"
        )
    except Exception as e:
        logger.error(f"上传招聘需求文档失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"上传招聘需求文档失败: {str(e)}"
        )
