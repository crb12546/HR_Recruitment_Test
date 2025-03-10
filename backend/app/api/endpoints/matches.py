"""
匹配API端点
"""
from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging
from app.db.session import get_db
from app.models.match import Match
from app.models.resume import Resume
from app.models.job_requirement import JobRequirement
from app.schemas.match import Match as MatchSchema, MatchCreate
from app.services.service_factory import get_ai_service
from app.utils.db_utils import safe_commit

# 获取日志记录器
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("", response_model=MatchSchema, status_code=status.HTTP_201_CREATED)
def create_match(
    *,
    db: Session = Depends(get_db),
    match_in: MatchCreate
) -> Any:
    """
    创建简历与职位匹配
    """
    try:
        # 记录请求数据
        logger.info(f"创建匹配请求: 简历ID={match_in.resume_id}, 职位ID={match_in.job_id}")
        
        # 检查简历是否存在
        resume = db.query(Resume).filter(Resume.id == match_in.resume_id).first()
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"简历不存在: ID={match_in.resume_id}"
            )
        
        # 检查职位是否存在
        job = db.query(JobRequirement).filter(JobRequirement.id == match_in.job_id).first()
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"职位不存在: ID={match_in.job_id}"
            )
        
        # 检查是否已存在匹配记录
        existing_match = db.query(Match).filter(
            Match.resume_id == match_in.resume_id,
            Match.job_id == match_in.job_id
        ).first()
        
        if existing_match:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"已存在匹配记录: ID={existing_match.id}"
            )
        
        # 初始化AI服务
        ai_service = get_ai_service()
        
        # 匹配简历与职位
        match_result = ai_service.match_resume_to_job(
            resume_content=resume.ocr_content,
            job_requirements=f"{job.position_name}\n{job.responsibilities}\n{job.requirements}"
        )
        
        # 创建匹配记录
        match = Match(
            resume_id=match_in.resume_id,
            job_id=match_in.job_id,
            match_score=match_result.get("score", 0),
            match_explanation=match_result.get("explanation", "")
        )
        
        # 保存到数据库
        db.add(match)
        if not safe_commit(db, "创建匹配记录失败"):
            raise HTTPException(status_code=500, detail="数据库保存失败")
        
        db.refresh(match)
        
        # 记录成功创建
        logger.info(f"成功创建匹配记录: ID={match.id}, 分数={match.match_score}")
        
        return match
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"数据库错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据库操作失败: {str(e)}"
        )
    except Exception as e:
        logger.error(f"创建匹配记录失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建匹配记录失败: {str(e)}"
        )

@router.get("", response_model=List[MatchSchema])
def read_matches(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    resume_id: Optional[int] = None,
    job_id: Optional[int] = None,
    min_score: Optional[float] = None
) -> Any:
    """
    获取匹配列表
    """
    try:
        # 构建查询
        query = db.query(Match)
        
        # 应用过滤条件
        if resume_id:
            query = query.filter(Match.resume_id == resume_id)
        if job_id:
            query = query.filter(Match.job_id == job_id)
        if min_score:
            query = query.filter(Match.match_score >= min_score)
        
        # 应用分页
        matches = query.order_by(Match.match_score.desc()).offset(skip).limit(limit).all()
        
        return matches
        
    except SQLAlchemyError as e:
        logger.error(f"数据库错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据库操作失败: {str(e)}"
        )
    except Exception as e:
        logger.error(f"获取匹配列表失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取匹配列表失败: {str(e)}"
        )

@router.get("/{match_id}", response_model=MatchSchema)
def read_match(
    *,
    db: Session = Depends(get_db),
    match_id: int
) -> Any:
    """
    获取匹配详情
    """
    try:
        # 查询匹配
        match = db.query(Match).filter(Match.id == match_id).first()
        if not match:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"匹配不存在: ID={match_id}"
            )
        
        return match
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"数据库错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据库操作失败: {str(e)}"
        )
    except Exception as e:
        logger.error(f"获取匹配详情失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取匹配详情失败: {str(e)}"
        )

@router.delete("/{match_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_match(
    *,
    db: Session = Depends(get_db),
    match_id: int
) -> Any:
    """
    删除匹配
    """
    try:
        # 查询匹配
        match = db.query(Match).filter(Match.id == match_id).first()
        if not match:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"匹配不存在: ID={match_id}"
            )
        
        # 删除匹配
        db.delete(match)
        if not safe_commit(db, f"删除匹配失败: ID={match_id}"):
            raise HTTPException(status_code=500, detail="数据库操作失败")
        
        # 记录成功删除
        logger.info(f"成功删除匹配: ID={match_id}")
        
        return None
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"数据库错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据库操作失败: {str(e)}"
        )
    except Exception as e:
        logger.error(f"删除匹配失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除匹配失败: {str(e)}"
        )

@router.post("/batch", response_model=List[MatchSchema])
def create_batch_matches(
    *,
    db: Session = Depends(get_db),
    job_id: int = Body(..., embed=True),
    resume_ids: List[int] = Body(..., embed=True)
) -> Any:
    """
    批量创建匹配
    """
    try:
        # 记录请求数据
        logger.info(f"批量创建匹配请求: 职位ID={job_id}, 简历IDs={resume_ids}")
        
        # 检查职位是否存在
        job = db.query(JobRequirement).filter(JobRequirement.id == job_id).first()
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"职位不存在: ID={job_id}"
            )
        
        # 初始化AI服务
        ai_service = get_ai_service()
        
        # 职位需求文本
        job_requirements = f"{job.position_name}\n{job.responsibilities}\n{job.requirements}"
        
        # 创建匹配记录
        matches = []
        for resume_id in resume_ids:
            # 检查简历是否存在
            resume = db.query(Resume).filter(Resume.id == resume_id).first()
            if not resume:
                logger.warning(f"简历不存在: ID={resume_id}")
                continue
            
            # 检查是否已存在匹配记录
            existing_match = db.query(Match).filter(
                Match.resume_id == resume_id,
                Match.job_id == job_id
            ).first()
            
            if existing_match:
                logger.warning(f"已存在匹配记录: ID={existing_match.id}")
                matches.append(existing_match)
                continue
            
            # 匹配简历与职位
            match_result = ai_service.match_resume_to_job(
                resume_content=resume.ocr_content,
                job_requirements=job_requirements
            )
            
            # 创建匹配记录
            match = Match(
                resume_id=resume_id,
                job_id=job_id,
                match_score=match_result.get("score", 0),
                match_explanation=match_result.get("explanation", "")
            )
            
            # 添加到数据库
            db.add(match)
            db.flush()
            
            matches.append(match)
        
        # 提交事务
        if not safe_commit(db, "批量创建匹配记录失败"):
            raise HTTPException(status_code=500, detail="数据库保存失败")
        
        # 记录成功创建
        logger.info(f"成功批量创建匹配记录: 数量={len(matches)}")
        
        return matches
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"数据库错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据库操作失败: {str(e)}"
        )
    except Exception as e:
        logger.error(f"批量创建匹配记录失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"批量创建匹配记录失败: {str(e)}"
        )
