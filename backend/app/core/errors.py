"""
错误处理模块
定义系统中使用的异常类和错误处理函数
"""
from typing import Any, Dict, Optional
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import Response
from starlette.exceptions import HTTPException as StarletteHTTPException

class BaseAppException(Exception):
    """应用基础异常类"""
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: Optional[Any] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.detail = detail
        super().__init__(self.message)

class DatabaseError(BaseAppException):
    """数据库错误"""
    def __init__(
        self,
        message: str = "数据库操作失败",
        detail: Optional[Any] = None,
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )

class NotFoundError(BaseAppException):
    """资源未找到错误"""
    def __init__(
        self,
        message: str = "请求的资源不存在",
        detail: Optional[Any] = None,
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )

class ValidationError(BaseAppException):
    """数据验证错误"""
    def __init__(
        self,
        message: str = "数据验证失败",
        detail: Optional[Any] = None,
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
        )

class AuthenticationError(BaseAppException):
    """认证错误"""
    def __init__(
        self,
        message: str = "认证失败",
        detail: Optional[Any] = None,
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )

class AuthorizationError(BaseAppException):
    """授权错误"""
    def __init__(
        self,
        message: str = "没有操作权限",
        detail: Optional[Any] = None,
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )

class AIServiceError(BaseAppException):
    """AI服务错误"""
    def __init__(
        self,
        message: str = "AI服务调用失败",
        detail: Optional[Any] = None,
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )

class FileServiceError(BaseAppException):
    """文件服务错误"""
    def __init__(
        self,
        message: str = "文件服务操作失败",
        detail: Optional[Any] = None,
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )

async def app_exception_handler(request: Request, exc: BaseAppException) -> JSONResponse:
    """应用异常处理器"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.message,
            "detail": exc.detail,
        },
    )

async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """HTTP异常处理器"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": str(exc.detail),
            "detail": None,
        },
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """验证异常处理器"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message": "数据验证失败",
            "detail": exc.errors(),
        },
    )

def register_exception_handlers(app: Any) -> None:
    """注册异常处理器"""
    app.add_exception_handler(BaseAppException, app_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
