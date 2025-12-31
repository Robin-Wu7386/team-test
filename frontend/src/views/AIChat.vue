<template>
  <div class="chat-page">
    <!-- 顶部装饰栏 -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-left">
          <!-- 返回首页按钮 -->
          <button @click="goToHome" class="back-home-btn">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M19 12H5M5 12L12 19M5 12L12 5" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>返回首页</span>
          </button>

          <!-- 清除历史按钮 -->
          <button @click="clearHistory" class="clear-history-btn" v-if="history.length > 0">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3 6H5H21" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M8 6V4C8 3.46957 8.21071 2.96086 8.58579 2.58579C8.96086 2.21071 9.46957 2 10 2H14C14.5304 2 15.0391 2.21071 15.4142 2.58579C15.7893 2.96086 16 3.46957 16 4V6M19 6V20C19 20.5304 18.7893 21.0391 18.4142 21.4142C18.0391 21.7893 17.5304 22 17 22H7C6.46957 22 5.96086 21.7893 5.58579 21.4142C5.21071 21.0391 5 20.5304 5 20V6H19Z" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M10 11V17" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M14 11V17" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>清除历史</span>
          </button>
        </div>

        <!-- logo区域 -->
        <div class="logo">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M2 17L12 22L22 17" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M2 12L12 17L22 12" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>AI 中医智能问诊</span>
        </div>

        <!-- 历史记录指示器 -->
        <div class="history-indicator" v-if="history.length > 0">
          <span class="history-count">对话记录: {{ history.length }} 条</span>
          <span class="history-tip">支持上下文记忆</span>
        </div>
      </div>
    </div>

    <div class="chat-container">
      <div class="chat-wrapper">
        <!-- 聊天头部 -->
        <div class="chat-header">
          <div class="avatar">
            <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="16" cy="16" r="15" fill="#f0f8f0" stroke="#43786a" stroke-width="1"/>
              <path d="M11 10C11 8.89543 11.8954 8 13 8H19C20.1046 8 21 8.89543 21 10V12C21 13.1046 20.1046 14 19 14H13C11.8954 14 11 13.1046 11 12V10Z" fill="#43786a"/>
              <path d="M7 19C7 15.6863 9.68629 13 13 13H19C22.3137 13 25 15.6863 25 19V20C25 21.1046 24.1046 22 23 22H9C7.89543 22 7 21.1046 7 20V19Z" fill="#43786a"/>
            </svg>
          </div>
          <div class="header-info">
            <h3>中医智能助手</h3>
            <p class="status">已就绪 · 专业辨证</p>
          </div>
        </div>

        <!-- 聊天内容区 -->
        <div class="chat-body" ref="chatBody">
          <!-- 欢迎卡片 -->
          <div class="welcome-card">
            <div class="card-content">
              <h4>🌿 欢迎使用 AI 中医智能问诊</h4>
              <p>请详细描述你的症状（如：乏力、头晕、手脚冰凉等），我将为你提供专业的中医辨证分析和调理建议。</p>
              <div class="quick-tips">
                <span class="tip-tag">示例：最近一周失眠多梦，口干舌燥</span>
                <span class="tip-tag">示例：持续头痛，伴有恶心症状</span>
                <span class="tip-tag">示例：长期疲劳，食欲不振</span>
              </div>
              <div class="ai-note">
                <span class="note-icon">📝</span>
                <span>我会专注于中医辨证分析，并提供中药、食疗等调理建议</span>
              </div>
            </div>
          </div>

          <!-- 聊天消息 -->
          <div v-for="(m,i) in messages" :key="i" :class="['msg',m.role]">
            <div class="msg-content">{{m.text}}</div>
            <div class="msg-time">{{formatTime(m.time)}}</div>
          </div>

          <!-- 加载状态 -->
          <div v-if="thinking" class="msg ai loading">
            <div class="loading-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <span class="loading-text">正在辨证分析...</span>
          </div>
        </div>

        <!-- 输入区 -->
        <div class="chat-input">
          <textarea
            v-model="input"
            @input="adjustTextareaHeight"
            placeholder="请详细描述你的症状，例如：最近一周容易疲劳，食欲不振，手脚冰凉..."
            @keydown.enter.exact="handleEnterSend"
            rows="1"
            ref="textareaRef"
          ></textarea>
          <button @click="send" :disabled="!input.trim() || thinking" class="send-btn">
            <svg v-if="!thinking" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M22 2L11 13" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="12" r="10" stroke="white" stroke-width="2" stroke-dasharray="60" stroke-dashoffset="0" class="loading-circle"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- 底部信息 -->
    <div class="page-footer">
      <p>© 2025 AI 中医智能问诊平台 | 本平台仅供参考，不构成医疗建议</p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick, onMounted, computed } from "vue";
import router from "@/router.js";

// 响应式数据
const input = ref("");
const messages = ref([]);
const thinking = ref(false);
const history = ref([]);
const chatBody = ref(null);
const textareaRef = ref(null);

// 系统Prompt - 控制AI只回答中医相关内容
const SYSTEM_PROMPT = `你是一位专业的中医专家，请严格遵守以下规则：
1. 专注于中医辨证论治，只回答与中医、中药、针灸、养生相关的问题
2. 对于非中医相关的问题，请礼貌回应："抱歉，我只专注于中医健康咨询"
3. 回答必须基于中医理论（阴阳五行、脏腑经络等）
4. 提供中药方剂时，要说明组成、功效和煎服方法
5. 建议食疗方案时，要说明食材的性味归经
6. 涉及穴位按摩时，要说明具体位置和按摩方法
7. 始终提醒用户：中医建议仅供参考，不能替代专业医疗诊断
8. 回答要专业、详细、有条理，体现中医特色

请基于以下对话历史进行辨证分析：`;

// 从localStorage加载历史记录
const loadHistory = () => {
  try {
    const saved = localStorage.getItem('tcm_chat_history');
    if (saved) {
      const parsed = JSON.parse(saved);
      return Array.isArray(parsed) ? parsed : [];
    }
  } catch (error) {
    console.error("加载历史记录失败:", error);
  }
  return [];
};

// 保存历史记录到localStorage
const saveHistory = (newHistory) => {
  try {
    // 限制历史记录长度，保留最近30条
    const limitedHistory = newHistory.slice(-30);
    localStorage.setItem('tcm_chat_history', JSON.stringify(limitedHistory));
  } catch (error) {
    console.error("保存历史记录失败:", error);
  }
};

// 计算历史记录摘要（用于提示词）
const getHistorySummary = () => {
  if (history.value.length === 0) return "";

  // 只取最近5条历史记录，避免提示词过长
  const recentHistory = history.value.slice(-5);
  return recentHistory.map(item =>
    `患者：${item.user}\n中医专家：${item.ai}`
  ).join('\n\n');
};

// 返回首页
const goToHome = () => {
  router.push('/');
};

// 清除历史记录
const clearHistory = () => {
  if (confirm('确定要清除所有对话历史吗？这将无法恢复。')) {
    history.value = [];
    saveHistory([]);
    messages.value = [{
      role: "ai",
      text: "对话历史已清除。我是你的中医智能问诊助手，请详细描述你的症状，我会为你提供专业的辨证分析和调理建议。",
      time: new Date()
    }];
  }
};

// 初始化消息
const initMessages = () => {
  const loadedHistory = loadHistory();
  history.value = loadedHistory;

  const now = new Date();

  if (loadedHistory.length > 0) {
    // 如果有历史记录，显示欢迎回来消息
    messages.value = [{
      role: "ai",
      text: "欢迎回来！我仍然是你专业的中医问诊助手。基于我们之前的交流，我了解你的基本情况。请继续描述症状，我会提供更精准的辨证分析。",
      time: now
    }];
  } else {
    // 没有历史记录时显示初始欢迎消息
    messages.value = [{
      role: "ai",
      text: "你好，我是你的中医智能问诊助手。请详细描述你的症状（如：乏力、头晕、手脚冰凉、食欲不振等），我会基于中医理论为你提供专业的辨证分析和中药调理建议。",
      time: now
    }];
  }
};

// 格式化时间
const formatTime = (date) => {
  return date.toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  });
};

// 滚动到底部
const scrollToBottom = () => {
  nextTick(() => {
    if (chatBody.value) {
      chatBody.value.scrollTop = chatBody.value.scrollHeight;
    }
  });
};

// 调整输入框高度
const adjustTextareaHeight = (e) => {
  const textarea = e.target;
  textarea.style.height = 'auto';
  const newHeight = Math.min(textarea.scrollHeight, 120);
  textarea.style.height = newHeight + 'px';
};

// 处理回车发送
const handleEnterSend = (e) => {
  if (e.shiftKey) {
    // Shift+Enter 换行
    return;
  }
  e.preventDefault();
  send();
};

// 发送消息到后端
const send = async () => {
  const text = input.value.trim();
  if (!text || thinking.value) return;

  const now = new Date();

  // 添加用户消息到显示
  messages.value.push({
    role: "user",
    text,
    time: now
  });

  // 清空输入框
  input.value = "";
  thinking.value = true;

  // 重置输入框高度
  if (textareaRef.value) {
    textareaRef.value.style.height = '44px';
  }

  scrollToBottom();

  try {
    // 构建完整请求数据
    const historySummary = getHistorySummary();
    const fullPrompt = `${SYSTEM_PROMPT}\n\n${historySummary}\n\n当前症状描述：${text}`;

    // 发送请求到后端
    const response = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        message: text,
        history: history.value,
        system_prompt: SYSTEM_PROMPT,
        full_prompt: fullPrompt
      })
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`HTTP ${response.status}: ${errorText}`);
    }

    const data = await response.json();
    const replyText = data.reply || "⚠️ 暂时无法提供回答，请稍后再试。";

    // 添加AI回复到显示
    messages.value.push({
      role: "ai",
      text: replyText,
      time: new Date()
    });

    // 更新历史记录
    history.value.push({
      user: text,
      ai: replyText,
      time: now.toISOString()
    });

    // 保存更新后的历史记录
    saveHistory(history.value);

  } catch (error) {
    console.error("请求失败：", error);

    // 提供友好的错误提示
    let errorMessage = "抱歉，系统暂时无法为你提供服务，请稍后再试。";

    if (error.message.includes('Failed to fetch')) {
      errorMessage = "无法连接到中医问诊服务，请检查：\n1. 后端服务是否启动（端口8000）\n2. 网络连接是否正常";
    } else if (error.message.includes('timeout')) {
      errorMessage = "辨证分析超时，建议简化症状描述后重试。";
    } else if (error.message.includes('500')) {
      errorMessage = "中医辨证系统内部错误，请稍后重试。";
    }

    messages.value.push({
      role: "ai",
      text: errorMessage,
      time: new Date()
    });

  } finally {
    thinking.value = false;
    scrollToBottom();
  }
};

// 监听消息变化，自动滚动到底部
watch(messages, scrollToBottom, { deep: true });

// 页面加载时初始化
onMounted(() => {
  initMessages();
  scrollToBottom();
});
</script>

<style scoped>
/* 全局样式重置和基础设置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: "Inter", "PingFang SC", "Microsoft YaHei", sans-serif;
}

.chat-page {
  width: 100vw;
  min-height: 100vh;
  background: linear-gradient(180deg, #f0f8f0 0%, #e6f5e6 100%);
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
}

/* 顶部装饰栏 */
.page-header {
  background: linear-gradient(90deg, #43786a 0%, #2d5d50 100%);
  padding: 16px 24px;
  color: white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

/* 返回首页按钮 */
.back-home-btn, .clear-history-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background-color: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  color: white;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.back-home-btn:hover, .clear-history-btn:hover {
  background-color: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.4);
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.back-home-btn:active, .clear-history-btn:active {
  transform: scale(0.98);
}

/* logo */
.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 18px;
  font-weight: 600;
}

/* 历史记录指示器 */
.history-indicator {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 13px;
  background: rgba(255, 255, 255, 0.1);
  padding: 6px 12px;
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.history-count {
  font-weight: 600;
}

.history-tip {
  opacity: 0.9;
  font-size: 12px;
}

/* 主容器 */
.chat-container {
  flex: 1;
  padding: 32px 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.chat-wrapper {
  width: 100%;
  max-width: 720px;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(67, 120, 106, 0.12);
  overflow: hidden;
  transition: all 0.3s ease;
}

.chat-wrapper:hover {
  box-shadow: 0 12px 40px rgba(67, 120, 106, 0.15);
}

/* 聊天头部 */
.chat-header {
  padding: 20px 24px;
  background: #f8fcf8;
  border-bottom: 1px solid #e8f0e8;
  display: flex;
  align-items: center;
  gap: 16px;
}

.avatar {
  flex-shrink: 0;
}

.header-info h3 {
  font-size: 18px;
  color: #2d5d50;
  font-weight: 600;
  margin-bottom: 4px;
}

.status {
  font-size: 12px;
  color: #6b8c82;
}

/* 聊天内容区 */
.chat-body {
  height: 60vh;
  max-height: 700px;
  padding: 24px;
  overflow-y: auto;
  background: #fafdfa;
  scroll-behavior: smooth;
}

/* 欢迎卡片 */
.welcome-card {
  margin-bottom: 24px;
  padding: 20px;
  background: linear-gradient(135deg, #e8f5e9 0%, #dceddc 100%);
  border-radius: 12px;
  border: 1px solid #d0e6d0;
}

.card-content h4 {
  color: #2d5d50;
  font-size: 16px;
  margin-bottom: 8px;
}

.card-content p {
  color: #43786a;
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 12px;
}

.quick-tips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;
}

.tip-tag {
  padding: 4px 12px;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 16px;
  font-size: 12px;
  color: #43786a;
  border: 1px solid rgba(67, 120, 106, 0.2);
}

.ai-note {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
  font-size: 12px;
  color: #2d5d50;
}

.note-icon {
  font-size: 14px;
}

/* 消息样式 */
.msg {
  max-width: 75%;
  margin-bottom: 16px;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

.msg-content {
  padding: 12px 16px;
  border-radius: 18px;
  line-height: 1.5;
  font-size: 14px;
  position: relative;
  white-space: pre-line;
}

.msg-time {
  font-size: 11px;
  margin-top: 4px;
  opacity: 0.7;
  transition: opacity 0.3s ease;
}

.msg:hover .msg-time {
  opacity: 1;
}

/* 用户消息 */
.msg.user {
  margin-left: auto;
}

.msg.user .msg-content {
  background: linear-gradient(90deg, #43786a 0%, #2d5d50 100%);
  color: white;
  border-bottom-right-radius: 4px;
}

.msg.user .msg-time {
  text-align: right;
  color: #6b8c82;
}

/* AI消息 */
.msg.ai .msg-content {
  background: #f0f8f0;
  color: #2d5d50;
  border: 1px solid #e8f0e8;
  border-bottom-left-radius: 4px;
}

.msg.ai .msg-time {
  text-align: left;
  color: #6b8c82;
}

/* 加载状态 */
.msg.loading {
  display: flex;
  align-items: center;
  gap: 8px;
}

.loading-dots {
  display: flex;
  gap: 4px;
}

.loading-dots span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #43786a;
  animation: bounce 1.4s infinite ease-in-out both;
}

.loading-dots span:nth-child(1) { animation-delay: -0.32s; }
.loading-dots span:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

.loading-text {
  color: #43786a;
  font-size: 14px;
}

/* 输入区 */
.chat-input {
  padding: 16px 24px;
  background: white;
  border-top: 1px solid #e8f0e8;
  display: flex;
  gap: 12px;
  align-items: flex-end;
}

.chat-input textarea {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid #e8f0e8;
  border-radius: 16px;
  outline: none;
  resize: none;
  font-size: 14px;
  color: #2d5d50;
  background: #f8fcf8;
  min-height: 44px;
  max-height: 120px;
  transition: border-color 0.2s ease;
  overflow-y: auto;
}

.chat-input textarea:focus {
  border-color: #43786a;
  box-shadow: 0 0 0 2px rgba(67, 120, 106, 0.1);
}

.chat-input textarea::placeholder {
  color: #99b3aa;
}

.send-btn {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: linear-gradient(90deg, #43786a 0%, #2d5d50 100%);
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  flex-shrink: 0;
  transition: all 0.2s ease;
}

.send-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.send-btn:not(:disabled):hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(67, 120, 106, 0.2);
}

/* 加载圆圈动画 */
.loading-circle {
  animation: rotate 1.5s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 底部信息 */
.page-footer {
  padding: 16px 24px;
  text-align: center;
  font-size: 12px;
  color: #6b8c82;
  background: transparent;
}

/* 滚动条美化 */
.chat-body::-webkit-scrollbar {
  width: 6px;
}

.chat-body::-webkit-scrollbar-track {
  background: #f8fcf8;
}

.chat-body::-webkit-scrollbar-thumb {
  background: #d0e6d0;
  border-radius: 3px;
}

.chat-body::-webkit-scrollbar-thumb:hover {
  background: #43786a;
}

/* 响应式适配 */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .header-left {
    width: 100%;
    justify-content: space-between;
  }

  .history-indicator {
    width: 100%;
    justify-content: space-between;
  }

  .chat-container {
    padding: 16px 10px;
  }

  .chat-body {
    height: 70vh;
    padding: 16px;
  }

  .welcome-card {
    padding: 16px;
  }

  .msg {
    max-width: 85%;
  }

  .chat-input {
    padding: 12px 16px;
  }
}
</style>