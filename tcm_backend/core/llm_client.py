# llm_client.py
import requests
from typing import Optional, Union, List, Dict


class VolcClient:
    """火山引擎API客户端（基本保持不变）"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
        self.timeout = 120

    def generate_answer(self, prompt_or_messages):
        if isinstance(prompt_or_messages, str):
            messages = [{"role": "user", "content": prompt_or_messages}]
        else:
            messages = prompt_or_messages

        data = {
            "model": "deepseek-v3-250324",
            "messages": messages
        }

        response = requests.post(
            url=self.api_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            },
            json=data,
            timeout=self.timeout
        )

        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()


class OllamaClient:
    """
    统一 Ollama Client：
    - 自动兼容【同事的 prompt-only API】
    - 自动兼容【Ollama 官方 /api/chat】
    """

    def __init__(self, api_url: str, model: str = "qwen2.5:14b"):
        self.api_url = api_url
        self.model = model
        self.timeout = 120

    def generate_answer(self, prompt_or_messages: Union[str, List[Dict]]):
        # 统一成 messages
        if isinstance(prompt_or_messages, str):
            messages = [{"role": "user", "content": prompt_or_messages}]
        else:
            messages = prompt_or_messages

        # ====== 关键：优先尝试 chat-completions（官方 Ollama） ======
        chat_payload = {
            "model": self.model,
            "messages": messages,
            "stream": False
        }

        try:
            r = requests.post(self.api_url, json=chat_payload, timeout=self.timeout)
            if r.status_code == 200:
                data = r.json()

                # 官方 Ollama 返回格式
                if "message" in data and "content" in data["message"]:
                    return data["message"]["content"].strip()

                # OpenAI 兼容格式
                if "choices" in data:
                    return data["choices"][0]["message"]["content"].strip()
        except Exception:
            pass  # 直接降级，不在这里报错

        # ====== 降级方案：prompt-only（同事 API） ======
        prompt = self._messages_to_prompt(messages)
        prompt_payload = {"prompt": prompt}

        r = requests.post(self.api_url, json=prompt_payload, timeout=self.timeout)
        r.raise_for_status()
        data = r.json()

        if "response" in data:
            return data["response"].strip()

        raise ValueError(f"Ollama API 返回格式无法识别: {data}")

    def _messages_to_prompt(self, messages: List[Dict]) -> str:
        """messages → prompt（给同事 API 用）"""
        lines = []
        for m in messages:
            if m["role"] == "system":
                lines.append(m["content"])
            elif m["role"] == "user":
                lines.append(f"问题：{m['content']}")
        lines.append("请直接给出专业回答。")
        return "\n\n".join(lines)
