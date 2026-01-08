from fastapi import FastAPI
import requests

app = FastAPI()


@app.post("/chat")
def chat(request: dict):
    """
    最简单的纯模型API
    接收任意格式，返回队友需要的格式
    """
    # 1. 提取问题内容
    prompt = ""

    if "message" in request:
        prompt = request["message"]
    elif "prompt" in request:
        prompt = request["prompt"]
    elif "messages" in request:
        messages = request["messages"]
        if isinstance(messages, list) and messages:
            if isinstance(messages[0], dict) and "content" in messages[0]:
                prompt = messages[0]["content"]
            elif isinstance(messages[0], str):
                prompt = messages[0]

    if not prompt:
        return {"response": "错误：没有找到问题内容"}

    # 2. 调用 Ollama
    try:
        ollama_response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "qwen2.5:14b",
                "messages": [{"role": "user", "content": prompt}],
                "stream": False
            },
            timeout=180
        )

        if ollama_response.status_code == 200:
            result = ollama_response.json()

            # 3. 提取回复内容
            if "message" in result and "content" in result["message"]:
                reply = result["message"]["content"]
            else:
                reply = str(result)

            # 4. 返回队友需要的格式
            return {"response": reply}
        else:
            return {"response": f"Ollama错误：{ollama_response.status_code}"}

    except requests.exceptions.ConnectionError:
        return {"response": "错误：Ollama服务未启动，请运行 ollama serve"}
    except Exception as e:
        return {"response": f"错误：{str(e)}"}


@app.get("/")
def home():
    return {
        "service": "纯模型API",
        "endpoint": "POST /chat",
        "格式": "返回 {'response': '模型回复'}"
    }


@app.get("/health")
def health():
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=5)
        return {"status": "ok", "ollama": "running"}
    except:
        return {"status": "error", "ollama": "not running"}