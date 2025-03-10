"""
主应用程序模块
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api import api_router
from app.core.config import settings
from app.core.errors import register_exception_handlers

def create_app() -> FastAPI:
    """创建FastAPI应用"""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.PROJECT_VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
    )

    # 设置CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 注册路由
    app.include_router(api_router, prefix=settings.API_V1_STR)

    # 注册异常处理器
    register_exception_handlers(app)

    # 健康检查端点
    @app.get("/api/health")
    def health_check():
        return {
            "status": "ok",
            "message": "HR招聘系统API服务正常运行",
            "path": "/api/health"
        }

    return app

app = create_app()
