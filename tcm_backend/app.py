# tcm_backend/app.py
from routers import qa
from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn
import jwt
import os

app = FastAPI(
    title="中医智能问答系统API",
    description="基于知识图谱和RAG的中医智能问答后端",
    version="1.0.0"
)

# JWT配置
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")  # 与backend/app.py保持一致
ALGORITHM = "HS256"

# 配置CORS：允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vue开发服务器
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建安全方案
security = HTTPBearer()

# JWT认证依赖
async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        # 验证token
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="无效的认证凭证")
        return {"user_id": user_id}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="登录已过期，请重新登录")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="无效的认证凭证")
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

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