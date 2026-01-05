from pydantic import BaseModel
import requests

class ChatRequest(BaseModel):
    message: str
    history: list | None = None

def chat_logic(req: ChatRequest):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5:7b-instruct-q5_K_M",
                "prompt": req.message,
                "stream": False
            },
            timeout=60
        )
        data = response.json()
        return {"reply": data.get("response", "⚠️ AI 未返回文本")}
    except Exception as e:
        print("调用 Ollama 出错:", e)
        return {"reply": "⚠️ AI 响应失败，请检查本地 Ollama 模型是否启动。"}
