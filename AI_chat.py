from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import requests

app = FastAPI()

# ===== CORS 设置 =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发阶段允许所有前端
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== 静态文件 =====
app.mount("/static", StaticFiles(directory="."), name="static")  # 当前目录

# ===== 请求模型 =====
class ChatRequest(BaseModel):
    message: str
    history: list | None = None

# ===== 聊天接口 =====
@app.post("/chat")
def chat(req: ChatRequest):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral:7b",
                "prompt": req.message,
                "stream": False
            },
            timeout=60
        )
        data = response.json()
        print("Ollama 返回:", data)

        reply_text = data.get("response", "⚠️ AI 未返回文本")
        return {"reply": reply_text}

    except Exception as e:
        print("调用 Ollama 出错:", e)
        return {"reply": "⚠️ AI 响应失败，请检查本地 Ollama 模型是否启动。"}

# ===== 首页返回 zhongyiyao.html =====
@app.get("/")
def index():
    return FileResponse("zhongyiyao.html")

# ===== AI 聊天页面 =====
@app.get("/chat_page")
def chat_page():
    return FileResponse("AI_chat.html")
