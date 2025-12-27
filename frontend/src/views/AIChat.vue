<template>
  <div class="chat-page">
    <!-- 顶部装饰栏（新增返回首页按钮） -->
    <div class="page-header">
      <div class="header-content">
        <!-- 返回首页按钮 -->
        <button @click="goToHome" class="back-home-btn">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M19 12H5M5 12L12 19M5 12L12 5" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>返回首页</span>
        </button>

        <!-- 原有logo区域 -->
        <div class="logo">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M2 17L12 22L22 17" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M2 12L12 17L22 12" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>AI 中医智能问诊</span>
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
            placeholder="请详细描述你的症状，例如：最近一周容易疲劳，食欲不振，手脚冰凉..."
            @keydown.enter.exact="handleEnterSend"
            rows="1"
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
import { ref, watch, nextTick } from "vue";
// 如果使用Vue Router，取消下面注释并确保已配置路由
// import { useRouter } from "vue-router";
// const router = useRouter();

const input = ref("");
const messages = ref([]);
const thinking = ref(false);
const history = ref([]);
const chatBody = ref(null);

// 返回首页函数
const goToHome = () => {
  // 方式1：使用Vue Router跳转（推荐，需提前配置首页路由）
  // router.push('/'); // 替换为你的首页路由路径，如 '/home'

  // 方式2：跳转到指定URL（适合无路由场景）
  window.location.href = '/'; // 替换为你的首页实际URL，如 'index.html'

  // 方式3：仅提示（测试用）
  // alert('返回首页');
};

// 初始化欢迎消息
const initMessages = () => {
  const now = new Date();
  messages.value = [
    {
      role:"ai",
      text:"你好，我是你的中医智能问诊助手。请详细描述你的症状，我会为你提供专业的辨证分析和调理建议。",
      time: now
    }
  ];
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

// 处理回车发送
const handleEnterSend = (e) => {
  e.preventDefault();
  send();
};

// 发送消息
const send = async () => {
  const text = input.value.trim();
  if(!text || thinking.value) return;

  const now = new Date();
  // 添加用户消息
  messages.value.push({
    role:"user",
    text,
    time: now
  });
  input.value = "";
  thinking.value = true;

  scrollToBottom();

  try {
    // 模拟接口请求（实际项目替换为真实接口）
    await new Promise(resolve => setTimeout(resolve, 2000));

    // 模拟AI回复
    const replyText = "根据你的症状描述，初步辨证为"+
      (Math.random() > 0.5 ? "气虚兼痰湿" : "肝郁气滞") +
      "体质。建议：1. 日常可食用"+
      (Math.random() > 0.5 ? "山药、薏米、茯苓" : "玫瑰花、陈皮、佛手") +
      "等食材调理；2. 避免熬夜，保持情绪舒畅；3. 适度进行八段锦、太极拳等温和运动。";

    // 添加AI回复
    messages.value.push({
      role:"ai",
      text: replyText,
      time: new Date()
    });

    // 更新历史记录
    history.value.push({
      user: text,
      ai: replyText,
      time: now
    });
  } catch (error) {
    messages.value.push({
      role:"ai",
      text:"抱歉，系统暂时无法为你提供服务，请稍后再试。",
      time: new Date()
    });
    console.error("请求失败：", error);
  } finally {
    thinking.value = false;
    scrollToBottom();
  }
};

// 监听消息变化，自动滚动到底部
watch(messages, scrollToBottom, { deep: true });

// 初始化
initMessages();
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

/* 顶部装饰栏 - 新增布局调整 */
.page-header {
  background: linear-gradient(90deg, #43786a 0%, #2d5d50 100%);
  padding: 16px 24px;
  color: white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* 返回首页按钮样式 */
.back-home-btn {
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

.back-home-btn:hover {
  background-color: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.4);
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.back-home-btn:active {
  transform: scale(0.98);
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 18px;
  font-weight: 600;
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
}

.tip-tag {
  padding: 4px 12px;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 16px;
  font-size: 12px;
  color: #43786a;
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
}

.msg-time {
  font-size: 11px;
  margin-top: 4px;
  opacity: 0.7;
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
}
</style>