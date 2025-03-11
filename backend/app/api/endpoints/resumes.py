"""
简历API端点
"""
from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging
from app.db.session import get_db
from app.models.resume import Resume
from app.models.tag import Tag
from app.schemas.resume import Resume as ResumeSchema, ResumeCreate, ResumeUpdate
from app.services.service_factory import get_ai_service, get_file_service
from app.utils.db_utils import safe_commit

# 获取日志记录器
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/upload", response_model=ResumeSchema, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    *,
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
    candidate_name: Optional[str] = Form(None)
) -> Any:
    """
    上传并解析简历
    """
    try:
        # 记录请求数据
        logger.info(f"上传简历请求: 文件名={file.filename}, 候选人={candidate_name}")
        
        # 获取文件服务
        file_service = get_file_service()
        
        # 上传文件
        file_info = await file_service.upload_file(file, folder="resumes")
        
        # 获取文件内容
        file_content = file_service.get_file_content(file_info["file_path"])
        content_str = file_content.decode("utf-8", errors="ignore")
        
        # 初始化AI服务
        ai_service = get_ai_service()
        
        # 解析简历内容
        parsed_content = ai_service.parse_resume(content_str)
        
        # 生成人才画像
        talent_portrait = ai_service.generate_talent_portrait(parsed_content)
        
        # 提取标签
        resume_tags = ai_service.generate_resume_tags(content_str)
        
        # 如果没有提供候选人姓名，使用解析结果
        if not candidate_name and parsed_content.get("name"):
            candidate_name = parsed_content.get("name")
        
        # 创建简历记录
        resume = Resume(
            candidate_name=candidate_name or "未知候选人",
            file_url=file_info["file_url"],
            file_type=file_info["file_type"],
            ocr_content=content_str,
            parsed_content=str(parsed_content),
            talent_portrait=talent_portrait
        )
        
        # 保存到数据库
        db.add(resume)
        if not safe_commit(db, "创建简历记录失败"):
            raise HTTPException(status_code=500, detail="数据库保存失败")
        
        # 添加标签
        for tag_name in resume_tags:
            # 查找或创建标签
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                tag = Tag(name=tag_name, category="skill")
                db.add(tag)
                db.flush()
            
            # 添加标签关联
            resume.tags.append(tag)
        
        if not safe_commit(db, "添加简历标签失败"):
            raise HTTPException(status_code=500, detail="数据库保存失败")
        
        db.refresh(resume)
        
        # 记录成功创建
        logger.info(f"成功创建简历记录: ID={resume.id}, 候选人={resume.candidate_name}")
        
        return resume
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"数据库错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据库操作失败: {str(e)}"
        )
    except Exception as e:
        logger.error(f"上传简历失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"上传简历失败: {str(e)}"
        )

@router.post("", response_model=ResumeSchema, status_code=status.HTTP_201_CREATED)
def create_resume(
    *,
    db: Session = Depends(get_db),
    resume_in: ResumeCreate
) -> Any:
    """
    创建简历
    """
    try:
        # 记录请求数据
        logger.info(f"创建简历请求: 候选人={resume_in.candidate_name}")
        
        # 创建简历记录
        resume = Resume(
            candidate_name=resume_in.candidate_name,
            file_url=resume_in.file_url,
            file_type=resume_in.file_type,
            ocr_content=resume_in.ocr_content,
            parsed_content=resume_in.parsed_content,
            talent_portrait=resume_in.talent_portrait
        )
        
        # 保存到数据库
        db.add(resume)
        if not safe_commit(db, "创建简历记录失败"):
            raise HTTPException(status_code=500, detail="数据库保存失败")
        
        db.refresh(resume)
        
        # 记录成功创建
        logger.info(f"成功创建简历记录: ID={resume.id}, 候选人={resume.candidate_name}")
        
        return resume
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"数据库错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据库操作失败: {str(e)}"
        )
    except Exception as e:
        logger.error(f"创建简历失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建简历失败: {str(e)}"
        )

@router.get("", response_model=List[ResumeSchema])
def read_resumes(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    candidate_name: Optional[str] = None,
    tag: Optional[str] = None
) -> Any:
    """
    获取简历列表
    """
    try:
        # 构建查询
        query = db.query(Resume)
        
        # 应用过滤条件
        if candidate_name:
            query = query.filter(Resume.candidate_name.ilike(f"%{candidate_name}%"))
        
        # 标签过滤
        if tag:
            query = query.join(Resume.tags).filter(Tag.name == tag)
        
        # 应用分页
        resumes = query.order_by(Resume.created_at.desc()).offset(skip).limit(limit).all()
        
        return resumes
        
    except SQLAlchemyError as e:
        logger.error(f"数据库错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据库操作失败: {str(e)}"
        )
    except Exception as e:
        logger.error(f"获取简历列表失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取简历列表失败: {str(e)}"
        )

@router.get("/{resume_id}", response_model=ResumeSchema)
def read_resume(
    *,
    db: Session = Depends(get_db),
    resume_id: int
) -> Any:
    """
    获取简历详情
    """
    try:
        # 查询简历
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"简历不存在: ID={resume_id}"
            )
        
        return resume
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"数据库错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据库操作失败: {str(e)}"
        )
    except Exception as e:
        logger.error(f"获取简历详情失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取简历详情失败: {str(e)}"
        )

@router.put("/{resume_id}", response_model=ResumeSchema)
def update_resume(
    *,
    db: Session = Depends(get_db),
    resume_id: int,
    resume_in: ResumeUpdate
) -> Any:
    """
    更新简历
    """
    try:
        # 查询简历
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"简历不存在: ID={resume_id}"
            )
        
        # 更新字段
        update_data = resume_in.model_dump(exclude_unset=True)
        
        # 应用更新
        for field, value in update_data.items():
            setattr(resume, field, value)
        
        # 保存到数据库
        if not safe_commit(db, f"更新简历失败: ID={resume_id}"):
            raise HTTPException(status_code=500, detail="数据库保存失败")
        
        db.refresh(resume)
        
        # 记录成功更新
        logger.info(f"成功更新简历: ID={resume.id}, 候选人={resume.candidate_name}")
        
        return resume
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"数据库错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据库操作失败: {str(e)}"
        )
    except Exception as e:
        logger.error(f"更新简历失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新简历失败: {str(e)}"
        )

@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resume(
    *,
    db: Session = Depends(get_db),
    resume_id: int
):
    """
    删除简历
    """
    try:
        # 查询简历
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"简历不存在: ID={resume_id}"
            )
        
        # 删除简历
        db.delete(resume)
        if not safe_commit(db, f"删除简历失败: ID={resume_id}"):
            raise HTTPException(status_code=500, detail="数据库操作失败")
        
        # 记录成功删除
        logger.info(f"成功删除简历: ID={resume_id}")
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"数据库错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据库操作失败: {str(e)}"
        )
    except Exception as e:
        logger.error(f"删除简历失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除简历失败: {str(e)}"
        )
