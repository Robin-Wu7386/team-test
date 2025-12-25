import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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

# ===== 静态文件挂载 =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ===== 首页 =====
@app.get("/")
def index():
    file_path = os.path.join(BASE_DIR, "zhongyiyao.html")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="主页文件不存在")
    return FileResponse(file_path)

# ===== 智能问诊页面 =====
@app.get("/chat_page")
def chat_page():
    file_path = os.path.join(BASE_DIR, "AI_chat.html")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="聊天页面文件不存在")
    return FileResponse(file_path)

# ===== 聊天接口 =====
@app.post("/chat")
def chat(req: ChatRequest):
    return chat_logic(req)

# ===== 测试接口 =====
@app.get("/test")
def test():
    return {"msg": "FastAPI 正常运行"}
