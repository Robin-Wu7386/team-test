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
          <span>老中医智能AI问诊</span>
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

        <!-- 新增：模型切换面板 -->
        <transition name="slide-fade">
          <div v-if="showSettings" class="settings-panel">
            <div class="panel-header">
              <h4>模型设置</h4>
              <button @click="showSettings = false" class="close-btn">×</button>
            </div>

            <div class="model-option"
                 :class="{ active: selectedModel === 'deepseek' }"
                 @click="selectedModel = 'deepseek'; showSettings = false; switchModel('deepseek')">
              <div class="model-title">DeepSeek-V3</div>
              <div class="model-desc">更强推理能力 · 回答更专业</div>
              <div class="tag-recommend">推荐</div>
            </div>

            <div class="model-option"
                 :class="{ active: selectedModel === 'ollama' }"
                 @click="selectedModel = 'ollama'; showSettings = false; switchModel('ollama')">
              <div class="model-title">本地模型（Ollama）</div>
              <div class="model-desc">响应更快 · 适合本地调试</div>
            </div>

            <div class="current-status">
              当前模型：<strong>{{ selectedModel === 'deepseek' ? 'DeepSeek-V3' : '本地Ollama模型' }}</strong>
            </div>
          </div>
        </transition>

        <!-- ========== 在这里插入模式面板 ========== -->
<transition name="slide-fade">
  <div v-if="showModePanel" class="mode-panel">
    <div class="panel-header">
      <h4>模式切换</h4>
      <button @click="showModePanel = false" class="close-btn">×</button>
    </div>

    <div class="mode-option"
         :class="{ active: selectedMode === 'pure_llm' }"
         @click="selectMode('pure_llm')">
      <div class="mode-icon">🤖</div>
      <div class="mode-info">
        <div class="mode-title">纯大模型模式</div>
        <div class="mode-desc">仅使用LLM自身知识</div>
      </div>
    </div>

    <div class="mode-option"
         :class="{ active: selectedMode === 'knowledge_graph' }"
         @click="selectMode('knowledge_graph')">
      <div class="mode-icon">📊</div>
      <div class="mode-info">
        <div class="mode-title">知识图谱模式</div>
        <div class="mode-desc">实体提取+知识图谱查询</div>
      </div>
    </div>

    <div class="mode-option"
         :class="{ active: selectedMode === 'rag_only' }"
         @click="selectMode('rag_only')">
      <div class="mode-icon">📚</div>
      <div class="mode-info">
        <div class="mode-title">RAG检索模式</div>
        <div class="mode-desc">古籍文献检索+LLM</div>
      </div>
    </div>

    <div class="mode-option"
         :class="{ active: selectedMode === 'full_function' }"
         @click="selectMode('full_function')">
      <div class="mode-icon">⚡</div>
      <div class="mode-info">
        <div class="mode-title">全功能模式</div>
        <div class="mode-desc">知识图谱+RAG+LLM（完整）</div>
      </div>
    </div>

    <div class="current-status">
      当前模式：<strong>{{ modeDisplayName }}</strong>
    </div>
  </div>
</transition>

        <!-- 聊天内容区 -->
        <div class="chat-body" ref="chatBody">
          <!-- 欢迎卡片 -->
          <div class="welcome-card">
            <div class="card-content">
              <h4>🌿 欢迎使用 老中医 智能AI问诊</h4>
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

<!-- ========== 在这里插入当前模式显示 ========== -->
<div class="current-mode-display">
  <span class="mode-tag" :class="selectedMode">{{ modeDisplayName }}</span>
  <button @click="toggleModePanel" class="mode-toggle-btn">
    {{ showModePanel ? '隐藏' : '切换模式' }}
  </button>
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
          <!-- 新增：右侧齿轮设置按钮 -->
        <div class="settings-toggle" @click="showSettings = !showSettings">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58a.49.49 0 0 0 .12-.61l-1.92-3.32a.49.49 0 0 0-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54a.49.49 0 0 0-.49-.42h-3.84a.49.49 0 0 0-.49.42l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96a.49.49 0 0 0-.59.22L2.74 8.87a.49.49 0 0 0 .12.61l2.03 1.58c-.05.3-.07.62-.07.94 0 .32.02.64.07.94l-2.03 1.58a.49.49 0 0 0-.12.61l1.92 3.32c.12.22.37.3.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.42.49.42h3.84c.25 0 .44-.18.49-.42l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32a.49.49 0 0 0-.12-.61l-2.03-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z" fill="#43786a"/>
          </svg>
        </div>

        <div class="mode-toggle" @click="toggleModePanel">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M3 17V7C3 5.89543 3.89543 5 5 5H19C20.1046 5 21 5.89543 21 7V17C21 18.1046 20.1046 19 19 19H5C3.89543 19 3 18.1046 3 17Z" stroke="#43786a" stroke-width="2"/>
    <path d="M8 9L12 13L16 9" stroke="#43786a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>

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
      <p>© 2026  老中医智能AI问诊平台 | 本平台仅供参考，不构成医疗建议</p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick, onMounted, computed } from "vue";
import router from "@/router.js";
import { tcmQaService } from '@/services/tcmQaService.js';
const selectedModel = ref('deepseek')  // 默认使用 DeepSeek-V3
const showSettings = ref(false)        // 控制设置面板显示
// 响应式数据
const input = ref("");
const messages = ref([]);
const thinking = ref(false);
const history = ref([]);
const chatBody = ref(null);
const textareaRef = ref(null);
// ========== 在这里添加模式相关数据 ==========
const selectedMode = ref('pure_llm')   // 默认纯LLM模式
const showModePanel = ref(false)       // 控制模式面板显示

// 添加计算属性
const modeDisplayName = computed(() => {
  const modeMap = {
    'pure_llm': '纯LLM',
    'knowledge_graph': '知识图谱',
    'rag_only': 'RAG检索',
    'full_function': '全功能'
  }
  return modeMap[selectedMode.value] || selectedMode.value
})

// ========== 修正后的 buildHistory 函数 ==========
const buildHistory = () => {
  const historyMessages = [];

  // 遍历消息，构建完整的 user-assistant 对话对
  for (let i = 0; i < messages.value.length; i++) {
    const msg = messages.value[i];

    if (msg.role === "user") {
      // 添加用户消息
      historyMessages.push({
        role: "user",
        content: msg.text
      });

      // 检查下一条消息是否是AI回复
      if (i + 1 < messages.value.length && messages.value[i + 1].role === "ai") {
        historyMessages.push({
          role: "assistant",  // OpenAI 格式
          content: messages.value[i + 1].text
        });
        i++; // 跳过已处理的AI消息
      } else {
        // 如果没有对应的AI回复，也添加一个空的assistant消息（保持对话对完整）
        historyMessages.push({
          role: "assistant",
          content: ""
        });
      }
    }
    // 忽略单独的AI消息（比如欢迎消息）
  }

  // 限制历史长度（保留最近3轮完整对话）
  // 注意：每个对话轮次包含 user + assistant 两条消息
  const maxRounds = 3;
  const maxMessages = maxRounds * 2;

  // 确保我们保留的是完整的对话对
  if (historyMessages.length > maxMessages) {
    // 从后往前取，确保是最近的完整对话
    const recentMessages = historyMessages.slice(-maxMessages);

    // 检查最后一条是否是assistant，如果不是则去掉最后一条
    if (recentMessages.length > 0 && recentMessages[recentMessages.length - 1].role !== "assistant") {
      return recentMessages.slice(0, -1);
    }
    return recentMessages;
  }

  return historyMessages;
};

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
    const limitedHistory = newHistory.slice(-5);
    localStorage.setItem('tcm_chat_history', JSON.stringify(limitedHistory));
  } catch (error) {
    console.error("保存历史记录失败:", error);
  }
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

const toggleModePanel = () => {
  showModePanel.value = !showModePanel.value
  // 切换时隐藏设置面板
  showSettings.value = false
}

const selectMode = (mode) => {
  selectedMode.value = mode
  showModePanel.value = false

  // 给用户友好提示
  const modeNames = {
    'pure_llm': '纯大模型模式（仅使用LLM自身知识）',
    'knowledge_graph': '知识图谱模式（实体提取+知识图谱查询）',
    'rag_only': 'RAG检索模式（古籍文献检索）',
    'full_function': '全功能模式（知识图谱+RAG+LLM）'
  }

  messages.value.push({
    role: "ai",
    text: `✅ 已切换到 ${modeNames[mode]}`,
    time: new Date()
  })
  scrollToBottom()
}

const switchModel = (model) => {
  // 给用户一个友好提示消息
  messages.value.push({
    role: "ai",
    text: `✅ 已切换到 ${model === 'deepseek' ? 'DeepSeek-V3（更强推理能力）' : '本地Ollama模型（响应更快）'}`,
    time: new Date()
  })
  scrollToBottom()
}

// ========== 修复后的 send 函数 ==========
const send = async () => {
  const text = input.value.trim();
  if (!text || thinking.value) return;

  const now = new Date();

  // ========== 关键修改：先构建历史，再添加当前消息 ==========
  let currentHistory = [];
  if (selectedMode.value === 'pure_llm') {
    // 只在 pure_llm 模式下构建历史记录
    currentHistory = buildHistory();
  }

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
    // ========== 关键修改：调用你自己的TCM系统 ==========
    const result = await tcmQaService.askQuestion(text, selectedModel.value, 3, currentHistory, selectedMode.value);

    let replyText;
    if (result.success) {
      replyText = result.answer;
    } else {
      replyText = `抱歉，系统处理遇到问题：${result.error || '未知错误'}`;
    }

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

    let errorMessage = "抱歉，系统暂时无法为你提供服务，请稍后再试。";

    if (error.message.includes('Failed to fetch') || error.message.includes('Network Error')) {
      errorMessage = "无法连接到中医问答服务，请检查：\n1. 后端服务是否启动（http://localhost:8001）\n2. 网络连接是否正常";
    } else if (error.message.includes('timeout')) {
      errorMessage = "问答系统处理超时，建议简化问题后重试。";
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

/* 右侧设置按钮和面板样式 */
.settings-toggle {
  width: 44px;
  height: 44px;
  background: rgba(67, 120, 106, 0.12);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-right: 8px; /* 和发送按钮保持一点间距 */
}

.settings-toggle:hover {
  background: rgba(67, 120, 106, 0.25);
  transform: rotate(60deg);
}

.settings-panel {
  position: absolute;
  top: 70px;
  right: 16px;
  width: 280px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 12px 40px rgba(0,0,0,0.18);
  padding: 16px;
  z-index: 100;
  border: 1px solid #e8f0e8;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.panel-header h4 {
  margin: 0;
  color: #2d5d50;
  font-size: 16px;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #aaa;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #666;
}

.model-option {
  padding: 14px;
  border-radius: 12px;
  cursor: pointer;
  margin-bottom: 10px;
  border: 2px solid transparent;
  transition: all 0.3s ease;
  position: relative;
  background: #f8fcf8;
}

.model-option:hover {
  background: #f0f8f0;
  border-color: #43786a;
}

.model-option.active {
  border-color: #43786a;
  background: #e8f5e9;
}

.model-title {
  font-weight: 600;
  color: #2d5d50;
  font-size: 15px;
}

.model-desc {
  font-size: 13px;
  color: #6b8c82;
  margin-top: 4px;
}

.tag-recommend {
  position: absolute;
  top: 10px;
  right: 10px;
  background: #43786a;
  color: white;
  font-size: 11px;
  padding: 3px 8px;
  border-radius: 6px;
}

.current-status {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #e8f0e8;
  text-align: center;
  color: #43786a;
  font-size: 14px;
}

/* 面板动画 */
.slide-fade-enter-active, .slide-fade-leave-active {
  transition: all 0.3s ease;
}
.slide-fade-enter-from, .slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}

.mode-panel {
  position: absolute;
  top: 70px;
  right: 16px;
  width: 300px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 12px 40px rgba(0,0,0,0.18);
  padding: 16px;
  z-index: 101;
  border: 1px solid #e8f0e8;
}

.mode-option {
  padding: 12px;
  border-radius: 12px;
  cursor: pointer;
  margin-bottom: 8px;
  border: 2px solid transparent;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 12px;
  background: #f8fcf8;
}

.mode-option:hover {
  background: #f0f8f0;
  border-color: #43786a;
}

.mode-option.active {
  border-color: #43786a;
  background: #e8f5e9;
}

.mode-icon {
  font-size: 20px;
  flex-shrink: 0;
}

.mode-info {
  flex: 1;
}

.mode-title {
  font-weight: 600;
  color: #2d5d50;
  font-size: 14px;
}

.mode-desc {
  font-size: 12px;
  color: #6b8c82;
  margin-top: 2px;
}

/* 当前模式显示区域 */
.current-mode-display {
  padding: 12px 24px;
  background: #f8fcf8;
  border-bottom: 1px solid #e8f0e8;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.mode-tag {
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 500;
}

.mode-tag.pure_llm {
  background: #e8f5e9;
  color: #2d5d50;
  border: 1px solid #c8e6c9;
}

.mode-tag.knowledge_graph {
  background: #e3f2fd;
  color: #1565c0;
  border: 1px solid #bbdefb;
}

.mode-tag.rag_only {
  background: #f3e5f5;
  color: #7b1fa2;
  border: 1px solid #e1bee7;
}

.mode-tag.full_function {
  background: #fff3e0;
  color: #ef6c00;
  border: 1px solid #ffcc80;
}

.mode-toggle-btn {
  padding: 6px 12px;
  background: rgba(67, 120, 106, 0.1);
  border: 1px solid rgba(67, 120, 106, 0.2);
  border-radius: 8px;
  color: #43786a;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.mode-toggle-btn:hover {
  background: rgba(67, 120, 106, 0.2);
}

/* 模式切换按钮样式 */
.mode-toggle {
  width: 44px;
  height: 44px;
  background: rgba(67, 120, 106, 0.12);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-right: 8px;
}

.mode-toggle:hover {
  background: rgba(67, 120, 106, 0.25);
  transform: rotate(180deg);
}

</style>