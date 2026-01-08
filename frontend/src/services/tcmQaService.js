// frontend/src/services/tcmQaService.js
import axios from 'axios';

// 注意：这里要改成你的后端实际地址
// 开发时用这个（代理或直接写全地址）：
const API_BASE_URL = 'http://localhost:8001/api';  // 直接写全地址，最保险

// 如果你用了 Vue 的 proxy，可以用 '/api'，但为了避免跨域问题，建议直接写全地址

const tcmApi = axios.create({
  baseURL: API_BASE_URL,
  timeout: 90000, // DeepSeek 可能需要更长时间，设 90 秒
  headers: { 'Content-Type': 'application/json' }
});

export const tcmQaService = {
  /**
   * 向中医问答系统提问（支持选择模型和模式）
   * @param {string} question - 用户问题
   * @param {string} model - "deepseek" 或 "ollama"，默认 deepseek
   * @param {number} topK - 检索文档数量，默认 3
   * @param {Array} history - 对话历史，默认 []
   * @param {string} mode - "pure_llm" | "knowledge_graph" | "rag_only" | "full_function"，默认 "pure_llm"
   */
  async askQuestion(question, model = 'deepseek', topK = 3, history = [], mode = 'pure_llm') {
    try {
      console.log('[TCM服务] 发送问题:', question,
                  '模型:', model,
                  '模式:', mode,
                  '历史长度:', history.length);

      const response = await tcmApi.post('/ask', {
        question,
        top_k_docs: topK,
        model,     // 模型选择
        history,   // 对话历史
        mode       // 新增：模式选择
      });

      console.log('[TCM服务] 收到响应:', response.data);
      return response.data;

    } catch (error) {
      console.error('[TCM服务] 调用失败:', error);
      let errorMsg = '抱歉，问答服务暂时不可用，请稍后重试。';

      if (error.code === 'ERR_NETWORK') {
        errorMsg = '无法连接到后端服务，请检查后端是否在运行（http://localhost:8001）';
      }

      return {
        success: false,
        query_id: 0,
        answer: errorMsg,
        user_question: question,
        path_type: 'error',
        current_model: model,
        mode: mode,  // 新增：返回当前模式
        error: error.message || '网络错误'
      };
    }
  }
};