# tcm_backend/app.py
from routers import qa
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="中医智能问答系统API",
    description="基于知识图谱和RAG的中医智能问答后端",
    version="1.0.0"
)

# 配置CORS：允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vue开发服务器
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(qa.router, prefix="/api", tags=["问答"])

@app.get("/")
async def root():
    return {"message": "中医智能问答系统后端服务已启动", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=False)