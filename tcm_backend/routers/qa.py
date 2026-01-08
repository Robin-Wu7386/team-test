# tcm_backend/routers/qa.py
from fastapi import APIRouter
from pydantic import BaseModel
import sys
import os

# 添加 core 目录到路径（因为 tcm_qa_system 在 core 里）
current_dir = os.path.dirname(os.path.abspath(__file__))
core_dir = os.path.join(current_dir, '..', 'core')
sys.path.insert(0, core_dir)

router = APIRouter()

try:
    from tcm_qa_system import TCMQASystem
    TCM_AVAILABLE = True
    print("✅ TCMQASystem 导入成功")
except ImportError as e:
    TCM_AVAILABLE = False
    print(f"❌ 导入失败: {e}")

class QuestionRequest(BaseModel):
    question: str
    top_k_docs: int = 3
    model: str = "deepseek"  # 新增：可选 "ollama" 或 "deepseek"
    history: list = []  # 新增：上下文历史记录
    mode: str = "pure_llm"  # 新增：模式选择，默认纯LLM模式

class QuestionResponse(BaseModel):
    success: bool
    query_id: int
    answer: str
    user_question: str
    path_type: str
    current_model: str
    history: list = []  # 新增：返回更新后的历史
    error: str = ""
    mode: str = "pure_llm"  # 新增：返回当前模式

# ==================== 请在这里填写你的真实配置 ====================
OLLAMA_API_URL = "https://prostomiate-bell-buildingless.ngrok-free.dev/chat"  # 你同事的本地模型地址（保持不变）
DEEPSEEK_API_KEY = "b68fab52-f4cd-4fb7-8c50-d67ccc8e6a12"  # ←←← 非常重要！替换成你的真实 Key

# 全局缓存不同的模型实例
_qa_systems = {
    "ollama": {},    # 改为空字典
    "deepseek": {}   # 改为空字典
}


def get_qa_system(model: str, mode: str = "pure_llm"):
    """获取问答系统实例，支持不同模式"""
    global _qa_systems
    if model not in ["ollama", "deepseek"]:
        raise ValueError("model 必须是 'ollama' 或 'deepseek'")

    # 验证模式参数
    valid_modes = ["pure_llm", "knowledge_graph", "rag_only", "full_function"]
    if mode not in valid_modes:
        raise ValueError(f"mode 必须是 {valid_modes} 之一")

    # 检查是否已有该模式的实例
    if model in _qa_systems and mode in _qa_systems[model]:
        return _qa_systems[model][mode]

    # 创建新实例
    print(f"正在初始化 {model.upper()} 模型，模式: {mode}")

    if model == "ollama":
        qa_system = TCMQASystem(
            show_prompt=True,
            llm_api_url=OLLAMA_API_URL,
            use_volc=False
        )
    else:  # deepseek
        if not DEEPSEEK_API_KEY or DEEPSEEK_API_KEY.startswith("请"):
            raise ValueError("DeepSeek API Key 未配置！")
        qa_system = TCMQASystem(
            show_prompt=True,
            llm_api_key=DEEPSEEK_API_KEY,
            use_volc=True
        )

    # 缓存实例
    _qa_systems[model][mode] = qa_system
    print(f"{model.upper()} 模式 {mode} 初始化完成")

    return qa_system

@router.post("/ask")
async def ask_question(request: QuestionRequest):
    try:
        if not TCM_AVAILABLE:
            return QuestionResponse(
                success=False,
                query_id=0,
                answer="",
                user_question=request.question,
                path_type="error",
                current_model=request.model,
                history=request.history,
                mode=request.mode,  # 返回请求的模式
                error="TCM系统加载失败"
            )

        # 验证模式参数
        valid_modes = ["pure_llm", "knowledge_graph", "rag_only", "full_function"]
        if request.mode not in valid_modes:
            return QuestionResponse(
                success=False,
                query_id=0,
                answer="",
                user_question=request.question,
                path_type="error",
                current_model=request.model,
                history=request.history,
                mode=request.mode,
                error=f"无效模式：{request.mode}，必须是 {valid_modes} 之一"
            )

        # 获取系统实例（传入模式参数）
        system = get_qa_system(request.model, request.mode)

        # 调用问答系统（现在支持模式参数）
        result = system.answer_question(
            user_question=request.question,
            top_k_docs=request.top_k_docs,
            history=request.history,
            mode=request.mode  # 传入模式参数
        )

        return QuestionResponse(
            success=True,
            query_id=result["query_id"],
            answer=result.get("final_answer", ""),
            user_question=result["user_question"],
            path_type=result["path_type"],
            current_model=request.model,
            history=request.history,
            mode=request.mode,  # 返回当前模式
            error=""
        )

    except ValueError as e:
        # 处理参数验证错误
        print(f"参数错误 [{request.model}/{request.mode}]: {e}")
        return QuestionResponse(
            success=False,
            query_id=0,
            answer="",
            user_question=request.question,
            path_type="error",
            current_model=request.model,
            history=request.history,
            mode=request.mode,
            error=str(e)[:200]
        )
    except Exception as e:
        print(f"问答错误 [{request.model}/{request.mode}]: {e}")
        return QuestionResponse(
            success=False,
            query_id=0,
            answer="",
            user_question=request.question,
            path_type="error",
            current_model=request.model,
            history=request.history,
            mode=request.mode,
            error=str(e)[:200]
        )


@router.get("/status")
async def status():
    """获取系统状态"""
    ollama_modes = list(_qa_systems.get("ollama", {}).keys())
    deepseek_modes = list(_qa_systems.get("deepseek", {}).keys())

    return {
        "tcm_available": TCM_AVAILABLE,
        "ollama_ready": len(ollama_modes) > 0,
        "deepseek_ready": len(deepseek_modes) > 0,
        "ollama_modes": ollama_modes,
        "deepseek_modes": deepseek_modes,
        "supported_modes": ["pure_llm", "knowledge_graph", "rag_only", "full_function"]
    }