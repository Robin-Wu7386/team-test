<template>
  <div class="chat-page">
    <!-- ===== 弹窗 (带过渡动画) ===== -->
    <transition name="fade">
      <div class="modal" v-if="showModal">
        <div class="modal-card">
          <div class="modal-header">
            <h2>🩺 基本信息填写</h2>
            <p class="subtitle">为了更准确的辩证，请完善您的档案</p>
          </div>

          <div class="form-grid">
            <div class="input-group">
              <label>年龄</label>
              <input type="number" v-model="age" placeholder="例如：28" />
            </div>

            <div class="input-group">
              <label>性别</label>
              <div class="gender-selector">
                <label :class="{ active: gender === '男' }">
                  <input type="radio" value="男" v-model="gender" />
                  <span>👨🏻 男</span>
                </label>
                <label :class="{ active: gender === '女' }">
                  <input type="radio" value="女" v-model="gender" />
                  <span>👩🏻 女</span>
                </label>
              </div>
            </div>

            <div class="row-inputs">
              <div class="input-group">
                <label>身高 (cm)</label>
                <input type="number" v-model="height" placeholder="175" />
              </div>
              <div class="input-group">
                <label>体重 (kg)</label>
                <input type="number" v-model="weight" placeholder="65" />
              </div>
            </div>
          </div>

          <button class="primary-btn" @click="confirmInfo">确认进入问诊</button>
        </div>
      </div>
    </transition>

    <!-- ===== 聊天主体 ===== -->
    <div class="chat-container">
      <div class="chat-card">
        <!-- 头部 -->
        <div class="chat-header">
          <div class="avatar-icon">🌿</div>
          <div class="header-info">
            <div class="title">AI 中医智能问诊</div>
            <div class="status">在线坐诊中</div>
          </div>
        </div>

        <!-- 消息区域 (增加了 ref 用于自动滚动) -->
        <div class="chat-body" ref="chatBodyRef">
          <div class="time-stamp">今天 {{ new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) }}</div>

          <div
            v-for="(m, i) in messages"
            :key="i"
            :class="['msg-row', m.role]"
          >
            <!-- AI 头像 -->
            <div v-if="m.role === 'ai'" class="msg-avatar ai-avatar">🌿</div>

            <div class="msg-bubble">
              {{ m.text }}
            </div>

            <!-- 用户头像 (可选，这里用简单的占位) -->
            <div v-if="m.role === 'user'" class="msg-avatar user-avatar">👤</div>
          </div>

          <!-- 思考状态 -->
          <div v-if="thinking" class="msg-row ai">
            <div class="msg-avatar ai-avatar">🌿</div>
            <div class="msg-bubble thinking-bubble">
              <span class="dot"></span><span class="dot"></span><span class="dot"></span>
            </div>
          </div>
        </div>

        <!-- 输入区域 -->
        <div class="chat-footer">
          <input
            v-model="input"
            placeholder="请详细描述您的症状（如：头痛、失眠...）"
            @keyup.enter="send"
          />
          <button @click="send" :disabled="!input || thinking">
            <span v-if="!thinking">发送</span>
            <span v-else>...</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from "vue";

/* ===== 基本信息逻辑 (保持不变) ===== */
const showModal = ref(true);
const age = ref("");
const gender = ref("");
const height = ref("");
const weight = ref("");

function confirmInfo() {
  if (!age.value || !gender.value) {
    alert("请至少填写年龄和性别");
    return;
  }
  showModal.value = false;
}

/* ===== 聊天逻辑 (保持不变，仅增加自动滚动) ===== */
const input = ref("");
const messages = ref([
  { role: "ai", text: "你好，我是你的中医智能问诊助手。请告诉我你哪里不舒服？" }
]);
const thinking = ref(false);
const history = ref([]);
const chatBodyRef = ref(null); // 用于滚动的DOM引用

// 辅助函数：滚动到底部
const scrollToBottom = () => {
  nextTick(() => {
    if (chatBodyRef.value) {
      chatBodyRef.value.scrollTop = chatBodyRef.value.scrollHeight;
    }
  });
};

async function send() {
  if (!input.value) return;

  // 添加用户消息
  messages.value.push({ role: "user", text: input.value });
  const userText = input.value;
  input.value = ""; // 立即清空输入框，提升体验
  scrollToBottom(); // 滚动

  thinking.value = true;
  scrollToBottom(); // 确保思考气泡可见

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: userText,
        history: history.value,
        profile: {
          age: age.value,
          gender: gender.value,
          height: height.value,
          weight: weight.value
        }
      })
    });

    const data = await res.json();
    thinking.value = false;
    messages.value.push({ role: "ai", text: data.reply });
    scrollToBottom(); // 收到消息后滚动
  } catch (e) {
    thinking.value = false;
    messages.value.push({ role: "ai", text: "网络连接似乎出了点问题，请稍后再试。" });
    scrollToBottom();
  }
}
</script>

<style scoped>
/*
  注意：这里使用了 var(--primary)
  如果 App.vue 里没有定义，这里提供一个默认值作为后备
*/
.chat-page {
  --primary-color: var(--primary, #42b983); /* 如果App.vue定义了primary则使用，否则使用绿色 */
  --bg-color: #f5f7fa;
  --bubble-ai: #ffffff;
  --bubble-user: var(--primary-color);

  min-height: 100vh;
  background-color: var(--bg-color);
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

/* ===== 弹窗样式优化 ===== */
.modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(5px); /* 磨砂玻璃背景 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
}

.modal-card {
  background: #fff;
  padding: 30px;
  border-radius: 24px;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  animation: slideUp 0.3s ease-out;
}

.modal-header h2 {
  margin: 0;
  color: #333;
  font-size: 1.5rem;
}

.subtitle {
  margin: 8px 0 20px;
  color: #666;
  font-size: 0.9rem;
}

.form-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 24px;
}

.input-group label {
  display: block;
  font-size: 0.85rem;
  font-weight: 600;
  color: #4a5568;
  margin-bottom: 6px;
}

.input-group input {
  width: 100%;
  padding: 12px;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.2s;
  box-sizing: border-box;
}

.input-group input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(66, 185, 131, 0.1);
}

.row-inputs {
  display: flex;
  gap: 15px;
}

/* 性别选择器美化 */
.gender-selector {
  display: flex;
  gap: 10px;
}

.gender-selector label {
  flex: 1;
  cursor: pointer;
  margin: 0;
}

.gender-selector input {
  display: none; /* 隐藏原生 radio */
}

.gender-selector span {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  color: #718096;
  transition: all 0.2s;
  font-weight: 500;
}

/* 选中状态 */
.gender-selector label.active span {
  background-color: var(--primary-color);
  color: #fff;
  border-color: var(--primary-color);
  box-shadow: 0 4px 6px -1px rgba(66, 185, 131, 0.3);
}

.primary-btn {
  width: 100%;
  padding: 14px;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.1s, opacity 0.2s;
}

.primary-btn:active {
  transform: scale(0.98);
}

/* ===== 聊天卡片 ===== */
.chat-container {
  width: 100%;
  max-width: 800px;
  padding: 20px;
  height: 100vh;
  box-sizing: border-box;
  display: flex;
  align-items: center;
}

.chat-card {
  width: 100%;
  height: 85vh; /* 固定高度，而不是靠内容撑开 */
  background: #fff;
  border-radius: 24px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

/* 头部 */
.chat-header {
  padding: 16px 24px;
  background: #fff;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar-icon {
  width: 40px;
  height: 40px;
  background: #e6fffa;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.header-info .title {
  font-weight: 700;
  font-size: 1.1rem;
  color: #2d3748;
}

.header-info .status {
  font-size: 0.8rem;
  color: var(--primary-color);
  display: flex;
  align-items: center;
  gap: 4px;
}

.header-info .status::before {
  content: "";
  display: block;
  width: 6px;
  height: 6px;
  background: var(--primary-color);
  border-radius: 50%;
}

/* 消息列表 */
.chat-body {
  flex: 1;
  background-color: #fcfcfc;
  padding: 20px;
  overflow-y: auto; /* 关键：只在这里滚动 */
  scroll-behavior: smooth;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.time-stamp {
  text-align: center;
  color: #cbd5e0;
  font-size: 0.75rem;
  margin-bottom: 10px;
}

.msg-row {
  display: flex;
  gap: 12px;
  align-items: flex-start;
  max-width: 85%;
}

.msg-row.user {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.msg-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-size: 18px;
}

.ai-avatar {
  background: #fff;
  border: 1px solid #eee;
}

.user-avatar {
  background: #edf2f7;
}

.msg-bubble {
  padding: 12px 16px;
  border-radius: 18px;
  line-height: 1.5;
  font-size: 0.95rem;
  position: relative;
  word-wrap: break-word;
}

.msg-row.ai .msg-bubble {
  background: var(--bubble-ai);
  color: #2d3748;
  border-top-left-radius: 4px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.03);
  border: 1px solid #f0f0f0;
}

.msg-row.user .msg-bubble {
  background: var(--bubble-user);
  color: #fff;
  border-top-right-radius: 4px;
  box-shadow: 0 4px 10px rgba(66, 185, 131, 0.2);
}

/* 思考中动画 */
.thinking-bubble {
  padding: 12px 20px;
  display: flex;
  gap: 4px;
  align-items: center;
}
.dot {
  width: 6px;
  height: 6px;
  background: #b0b0b0;
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out both;
}
.dot:nth-child(1) { animation-delay: -0.32s; }
.dot:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

/* 底部输入栏 */
.chat-footer {
  padding: 16px 24px;
  background: #fff;
  border-top: 1px solid #f0f0f0;
  display: flex;
  gap: 12px;
  align-items: center;
}

.chat-footer input {
  flex: 1;
  padding: 12px 16px;
  background: #f7fafc;
  border: 1px solid #edf2f7;
  border-radius: 24px;
  font-size: 0.95rem;
  transition: border 0.2s;
}

.chat-footer input:focus {
  outline: none;
  background: #fff;
  border-color: var(--primary-color);
}

.chat-footer button {
  padding: 10px 24px;
  background: var(--primary-color);
  color: #fff;
  border: none;
  border-radius: 24px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
  min-width: 80px;
}

.chat-footer button:hover {
  opacity: 0.9;
}

.chat-footer button:disabled {
  background: #cbd5e0;
  cursor: not-allowed;
}

/* 简单的进入动画 */
@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>