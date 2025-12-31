import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import requests
from pydantic import BaseModel
from typing import List, Dict, Optional

app = FastAPI()

# CORS设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# 数据模型
class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Dict]] = None


class ChatResponse(BaseModel):
    reply: str
    status: str = "success"


# 中医专用提示词
TCM_PROMPT = """你是一位中医专家，请遵守：
1. 只回答中医、中药、针灸、养生相关问题
2. 非中医问题请礼貌拒绝
3. 基于中医理论回答
4. 提供中药方剂要说明组成和用法
5. 食疗建议要说明食材性味
6. 提醒用户：中医建议仅供参考

历史对话："""


# 构建完整提示词
def build_prompt(message: str, history: Optional[List[Dict]] = None) -> str:
    prompt = TCM_PROMPT

    if history and len(history) > 0:
        # 取最近3条历史
        for item in history[-3:]:
            prompt += f"\n患者：{item.get('user', '')}"
            prompt += f"\n中医专家：{item.get('ai', '')}\n"

    prompt += f"\n当前患者：{message}"
    prompt += "\n\n请以中医专家身份回答："

    return prompt


# 调用Ollama
def call_ollama(prompt: str) -> str:
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral:7b",
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.7, "num_predict": 512}
            },
            timeout=60
        )

        if response.status_code == 200:
            data = response.json()
            return data.get("response", "⚠️ AI未返回内容")
        else:
            return "抱歉，中医辨证系统暂时无法响应"

    except requests.exceptions.ConnectionError:
        return "中医辨证服务未启动，请检查Ollama服务"
    except requests.exceptions.Timeout:
        return "辨证分析超时，请简化描述后重试"
    except Exception as e:
        print(f"调用Ollama出错: {e}")
        return "中医系统异常，请稍后重试"


# 路由
@app.get("/")
def index():
    return {"msg": "中医问诊API运行中"}


@app.post("/chat")
def chat(req: ChatRequest) -> ChatResponse:
    try:
        # 构建提示词（包含历史记忆）
        prompt = build_prompt(req.message, req.history)

        # 调用Ollama
        reply = call_ollama(prompt)

        return ChatResponse(reply=reply)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/test")
def test():
    return {"msg": "API正常"}