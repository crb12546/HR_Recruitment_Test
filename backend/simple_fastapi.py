import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 创建FastAPI应用
app = FastAPI(
    title="HR招聘系统API",
    description="HR招聘系统后端API服务",
    version="0.1.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 健康检查端点
@app.get("/")
def root():
    return {"message": "HR招聘系统API服务正常运行"}

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "服务正常运行"}

# 启动服务器
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
