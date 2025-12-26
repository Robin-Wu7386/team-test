import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from AI_chat import chat_logic, ChatRequest

app = FastAPI()

# ===== CORS 设置 =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== 静态文件（给 Vue 用图片）=====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ===== 根路由（后端提示用）=====
@app.get("/")
def index():
    return {
        "msg": "FastAPI 后端接口运行中",
        "usage": {
            "frontend": "http://localhost:5173",
            "chat_api": "POST /chat",
            "test": "/test"
        }
    }

# ===== 聊天接口（Vue 调用）=====
@app.post("/chat")
def chat(req: ChatRequest):
    return chat_logic(req)

# ===== 测试接口 =====
@app.get("/test")
def test():
    return {"msg": "FastAPI 正常运行"}
