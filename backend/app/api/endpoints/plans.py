"""
招聘方案API端点
"""
from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging
from app.db.session import get_db
from app.models.plan import Plan
from app.models.job_requirement import JobRequirement
from app.models.match import Match
from app.models.resume import Resume
from app.schemas.plan import Plan as PlanSchema, PlanCreate, PlanUpdate
from app.services.service_factory import get_ai_service
from app.utils.db_utils import safe_commit

# 获取日志记录器
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("", response_model=PlanSchema, status_code=status.HTTP_201_CREATED)
def create_plan(
    *,
    db: Session = Depends(get_db),
    plan_in: PlanCreate
) -> Any:
    """
    创建招聘方案
    """
    try:
        # 记录请求数据
        logger.info(f"创建招聘方案请求: 职位ID={plan_in.job_id}")
        
        # 检查职位是否存在
        job = db.query(JobRequirement).filter(JobRequirement.id == plan_in.job_id).first()
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"职位不存在: ID={plan_in.job_id}"
            )
        
        # 创建招聘方案
        plan = Plan(
            title=plan_in.title,
            job_id=plan_in.job_id,
            description=plan_in.description,
            strategy=plan_in.strategy,
            candidate_ids=plan_in.candidate_ids
        )
        
        # 保存到数据库
        db.add(plan)
        if not safe_commit(db, "创建招聘方案失败"):
            raise HTTPException(status_code=500, detail="数据库保存失败")
        
        db.refresh(plan)
        
        # 记录成功创建
        logger.info(f"成功创建招聘方案: ID={plan.id}, 标题={plan.title}")
        
        return plan
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"数据库错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据库操作失败: {str(e)}"
        )
    except Exception as e:
        logger.error(f"创建招聘方案失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建招聘方案失败: {str(e)}"
        )

@router.get("", response_model=List[PlanSchema])
def read_plans(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    job_id: Optional[int] = None
) -> Any:
    """
    获取招聘方案列表
    """
    try:
        # 构建查询
        query = db.query(Plan)
        
        # 应用过滤条件
        if job_id:
            query = query.filter(Plan.job_id == job_id)
        
        # 应用分页
        plans = query.order_by(Plan.created_at.desc()).offset(skip).limit(limit).all()
        
        return plans
        
    except SQLAlchemyError as e:
        logger.error(f"数据库错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据库操作失败: {str(e)}"
        )
    except Exception as e:
        logger.error(f"获取招聘方案列表失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取招聘方案列表失败: {str(e)}"
        )

@router.get("/{plan_id}", response_model=PlanSchema)
def read_plan(
    *,
    db: Session = Depends(get_db),
    plan_id: int
) -> Any:
    """
    获取招聘方案详情
    """
    try:
        # 查询招聘方案
        plan = db.query(Plan).filter(Plan.id == plan_id).first()
        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"招聘方案不存在: ID={plan_id}"
            )
        
        return plan
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"数据库错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据库操作失败: {str(e)}"
        )
    except Exception as e:
        logger.error(f"获取招聘方案详情失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取招聘方案详情失败: {str(e)}"
        )

@router.put("/{plan_id}", response_model=PlanSchema)
def update_plan(
    *,
    db: Session = Depends(get_db),
    plan_id: int,
    plan_in: PlanUpdate
) -> Any:
    """
    更新招聘方案
    """
    try:
        # 查询招聘方案
        plan = db.query(Plan).filter(Plan.id == plan_id).first()
        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"招聘方案不存在: ID={plan_id}"
            )
        
        # 更新字段
        update_data = plan_in.dict(exclude_unset=True)
        
        # 应用更新
        for field, value in update_data.items():
            setattr(plan, field, value)
        
        # 保存到数据库
        if not safe_commit(db, f"更新招聘方案失败: ID={plan_id}"):
            raise HTTPException(status_code=500, detail="数据库保存失败")
        
        db.refresh(plan)
        
        # 记录成功更新
        logger.info(f"成功更新招聘方案: ID={plan.id}, 标题={plan.title}")
        
        return plan
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"数据库错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据库操作失败: {str(e)}"
        )
    except Exception as e:
        logger.error(f"更新招聘方案失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新招聘方案失败: {str(e)}"
        )

@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_plan(
    *,
    db: Session = Depends(get_db),
    plan_id: int
):
    """
    删除招聘方案
    """
    try:
        # 查询招聘方案
        plan = db.query(Plan).filter(Plan.id == plan_id).first()
        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"招聘方案不存在: ID={plan_id}"
            )
        
        # 删除招聘方案
        db.delete(plan)
        if not safe_commit(db, f"删除招聘方案失败: ID={plan_id}"):
            raise HTTPException(status_code=500, detail="数据库操作失败")
        
        # 记录成功删除
        logger.info(f"成功删除招聘方案: ID={plan_id}")
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"数据库错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据库操作失败: {str(e)}"
        )
    except Exception as e:
        logger.error(f"删除招聘方案失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除招聘方案失败: {str(e)}"
        )

@router.post("/generate", response_model=PlanSchema)
def generate_plan(
    *,
    db: Session = Depends(get_db),
    job_id: int = Body(..., embed=True),
    min_score: float = Body(70.0, embed=True),
    title: str = Body(..., embed=True)
) -> Any:
    """
    自动生成招聘方案
    """
    try:
        # 记录请求数据
        logger.info(f"自动生成招聘方案请求: 职位ID={job_id}, 最低分数={min_score}")
        
        # 检查职位是否存在
        job = db.query(JobRequirement).filter(JobRequirement.id == job_id).first()
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"职位不存在: ID={job_id}"
            )
        
        # 查询匹配的简历
        matches = db.query(Match).filter(
            Match.job_id == job_id,
            Match.match_score >= min_score
        ).order_by(Match.match_score.desc()).all()
        
        if not matches:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"没有找到匹配分数大于{min_score}的简历"
            )
        
        # 初始化AI服务
        ai_service = get_ai_service()
        
        # 准备匹配简历数据
        matched_resumes = []
        for match in matches:
            resume = db.query(Resume).filter(Resume.id == match.resume_id).first()
            if resume:
                matched_resumes.append({
                    "resume_id": resume.id,
                    "candidate_name": resume.candidate_name,
                    "talent_portrait": resume.talent_portrait,
                    "match_score": match.match_score,
                    "match_explanation": match.match_explanation
                })
        
        # 生成招聘方案
        plan_data = ai_service.generate_recruitment_plan(
            job_requirement=job.to_dict(),
            matched_resumes=matched_resumes
        )
        
        # 创建招聘方案
        plan = Plan(
            title=title,
            job_id=job_id,
            description=plan_data.get("description", ""),
            strategy=plan_data.get("recruitment_strategy", ""),
            candidate_ids=[rec.get("candidate_id") for rec in plan_data.get("candidate_recommendations", [])]
        )
        
        # 保存到数据库
        db.add(plan)
        if not safe_commit(db, "创建招聘方案失败"):
            raise HTTPException(status_code=500, detail="数据库保存失败")
        
        db.refresh(plan)
        
        # 记录成功创建
        logger.info(f"成功自动生成招聘方案: ID={plan.id}, 标题={plan.title}")
        
        return plan
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"数据库错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据库操作失败: {str(e)}"
        )
    except Exception as e:
        logger.error(f"自动生成招聘方案失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"自动生成招聘方案失败: {str(e)}"
        )
