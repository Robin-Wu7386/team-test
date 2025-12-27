<template>
  <div class="chat-page">
    <!-- 背景纹理 -->
    <div class="bg-pattern"></div>

    <!-- ===== 1. 健康档案弹窗 (Glassmorphism 玻璃拟态) ===== -->
    <transition name="modal-fade">
      <div class="modal-overlay" v-if="showModal">
        <div class="modal-card">
          <div class="modal-decoration"></div>

          <div class="card-header">
            <div class="icon-box">
              <i class="ri-pulse-line"></i>
            </div>
            <div class="header-text">
              <h2>建立健康档案</h2>
              <p>AI 辨证需要您的基础体征数据</p>
            </div>
          </div>

          <div class="form-body">
            <!-- 年龄与性别 -->
            <div class="row-group">
              <div class="input-group">
                <label>年龄</label>
                <input type="number" v-model="age" placeholder="25" class="clean-input" />
              </div>

              <div class="input-group">
                <label>性别</label>
                <div class="gender-toggle">
                  <div class="toggle-track" :class="{ right: gender === '女' }"></div>
                  <div class="toggle-option" :class="{ active: gender === '男' }" @click="gender = '男'">男</div>
                  <div class="toggle-option" :class="{ active: gender === '女' }" @click="gender = '女'">女</div>
                </div>
              </div>
            </div>

            <!-- 身高与体重 -->
            <div class="row-group">
              <div class="input-group">
                <label>身高 <span class="unit">(cm)</span></label>
                <input type="number" v-model="height" placeholder="175" class="clean-input" />
              </div>
              <div class="input-group">
                <label>体重 <span class="unit">(kg)</span></label>
                <input type="number" v-model="weight" placeholder="65" class="clean-input" />
              </div>
            </div>
          </div>

          <button class="start-btn" @click="confirmInfo">
            <span>生成档案并问诊</span>
            <i class="ri-arrow-right-line"></i>
          </button>
        </div>
      </div>
    </transition>

    <!-- ===== 2. 聊天主界面 ===== -->
    <div class="chat-container">
      <!-- 侧边装饰/功能区 (可选，这里做装饰) -->
      <div class="side-panel">
        <div class="brand">岐黄</div>
        <div class="active-indicator">
          <span></span><span></span><span></span>
        </div>
      </div>

      <!-- 聊天窗口 -->
      <div class="chat-main-window">
        <!-- 顶部状态栏 -->
        <header class="chat-header">
          <div class="ai-profile">
            <div class="avatar-ring">
              <img src="https://api.dicebear.com/7.x/notionists/svg?seed=TCM_AI" alt="AI" />
            </div>
            <div class="ai-meta">
              <h3>岐黄智能医师</h3>
              <div class="status-badge">
                <span class="dot"></span> 深度学习模型运行中
              </div>
            </div>
          </div>
          <div class="window-actions">
            <button class="action-btn" title="清空对话" @click="messages = []"><i class="ri-delete-bin-line"></i></button>
            <button class="action-btn" @click="$router.push('/')" title="返回首页"><i class="ri-home-4-line"></i></button>
          </div>
        </header>

        <!-- 消息流区域 -->
        <div class="message-area" ref="chatBodyRef">
          <div class="session-start">
            <span class="date-tag">{{ new Date().toLocaleDateString() }} · 望闻问切</span>
          </div>

          <div
            v-for="(msg, index) in messages"
            :key="index"
            class="message-wrapper"
            :class="msg.role"
          >
            <!-- AI 消息 -->
            <template v-if="msg.role === 'ai'">
              <div class="avatar ai-avatar">
                <i class="ri-medicine-bottle-line"></i>
              </div>
              <div class="bubble ai-bubble">
                <div class="bubble-text">{{ msg.text }}</div>
              </div>
            </template>

            <!-- 用户消息 -->
            <template v-if="msg.role === 'user'">
              <div class="bubble user-bubble">
                <div class="bubble-text">{{ msg.text }}</div>
              </div>
              <div class="avatar user-avatar">
                <i class="ri-user-3-line"></i>
              </div>
            </template>
          </div>

          <!-- 思考加载态 -->
          <div v-if="thinking" class="message-wrapper ai">
            <div class="avatar ai-avatar"><i class="ri-brain-line"></i></div>
            <div class="bubble ai-bubble thinking-bubble">
              <div class="typing-indicator">
                <span></span><span></span><span></span>
              </div>
              <span class="thinking-text">正在辨证分析...</span>
            </div>
          </div>
        </div>

        <!-- 底部输入区 -->
        <footer class="input-footer">
          <div class="input-wrapper">
            <input
              v-model="input"
              type="text"
              placeholder="请详细描述您的症状（如：头痛、舌苔颜色、睡眠情况）..."
              @keyup.enter="send"
              :disabled="thinking"
            />
            <button class="send-btn" @click="send" :disabled="!input || thinking">
              <i class="ri-send-plane-fill"></i>
            </button>
          </div>
        </footer>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from "vue";
import { useRouter } from 'vue-router';

// 如果没有全局引入 RemixIcon，可以在这里引入，或者在 index.html 引入
// import 'remixicon/fonts/remixicon.css';

const router = useRouter();

// --- 档案逻辑 ---
const showModal = ref(true);
const age = ref("");
const gender = ref("男"); // 默认选中男
const height = ref("");
const weight = ref("");

function confirmInfo() {
  if (!age.value) {
    // 简单的震动提示或者是 alert
    alert("请填写年龄以便更精准的诊断");
    return;
  }
  showModal.value = false;
}

// --- 聊天逻辑 ---
const input = ref("");
const thinking = ref(false);
const chatBodyRef = ref(null);
const history = ref([]);

const messages = ref([
  { role: "ai", text: "您好，我是岐黄 AI 医师。望闻问切，首重于问。请告诉我您哪里不舒服？" }
]);

const scrollToBottom = () => {
  nextTick(() => {
    if (chatBodyRef.value) {
      chatBodyRef.value.scrollTo({
        top: chatBodyRef.value.scrollHeight,
        behavior: "smooth"
      });
    }
  });
};

async function send() {
  if (!input.value.trim()) return;

  const userText = input.value;
  messages.value.push({ role: "user", text: userText });
  input.value = "";
  scrollToBottom();

  thinking.value = true;
  scrollToBottom();

  try {
    // 模拟后端请求结构，实际对接时请使用你的真实URL
    const res = await fetch("/chat", { // 假设你的后端地址
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

    // 简单的历史记录维护
    history.value.push({ role: "user", content: userText });
    history.value.push({ role: "assistant", content: data.reply });

    thinking.value = false;
    messages.value.push({ role: "ai", text: data.reply });
    scrollToBottom();

  } catch (e) {
    console.error(e);
    thinking.value = false;
    // 模拟错误回复，用于演示
    setTimeout(() => {
        messages.value.push({ role: "ai", text: "脉象紊乱（网络连接超时），请检查网络后重试。" });
        scrollToBottom();
    }, 1000);
  }
}
</script>

<style scoped>
/*
  导入 Google Fonts - 衬线体增加医学权威感
*/
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&family=Inter:wght@400;600&display=swap');
@import url("https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css");

/* ====== 全局容器 ====== */
.chat-page {
  position: relative;
  width: 100vw;
  height: 100vh;
  background-color: #f0f4f3; /* 极淡的草药灰绿 */
  font-family: 'Noto Serif SC', 'Inter', serif;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 背景纹理：细微的方格纸效果，模拟处方笺 */
.bg-pattern {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background-image:
    linear-gradient(rgba(44, 92, 77, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(44, 92, 77, 0.03) 1px, transparent 1px);
  background-size: 40px 40px;
  z-index: 0;
}

/* ====== 1. Modal 弹窗设计 ====== */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(20, 30, 25, 0.4); /* 深色遮罩 */
  backdrop-filter: blur(8px);
  z-index: 1000;
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-card {
  width: 90%;
  max-width: 420px;
  background: #ffffff;
  border-radius: 24px;
  padding: 32px;
  position: relative;
  box-shadow:
    0 20px 50px rgba(44, 92, 77, 0.15),
    0 0 0 1px rgba(255, 255, 255, 1);
  overflow: hidden;
}

/* 顶部装饰条 */
.modal-decoration {
  position: absolute;
  top: 0; left: 0; width: 100%; height: 6px;
  background: linear-gradient(90deg, #2c5c4d, #6fbf9a);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 30px;
}

.icon-box {
  width: 48px; height: 48px;
  background: #e6f2ed;
  color: #2c5c4d;
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  font-size: 24px;
}

.header-text h2 { margin: 0; font-size: 20px; color: #1a1a1a; font-weight: 700; }
.header-text p { margin: 4px 0 0; font-size: 13px; color: #888; font-family: 'Inter', sans-serif; }

.row-group {
  display: flex; gap: 16px; margin-bottom: 20px;
}

.input-group { flex: 1; }
.input-group label {
  display: block; font-size: 12px; font-weight: 600; color: #555; margin-bottom: 8px; font-family: 'Inter', sans-serif;
}
.unit { color: #999; font-weight: normal; }

.clean-input {
  width: 100%;
  padding: 12px;
  background: #f7f9f8;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  font-size: 16px;
  color: #333;
  transition: all 0.3s;
  font-family: 'Inter', sans-serif;
}
.clean-input:focus {
  background: #fff;
  border-color: #2c5c4d;
  box-shadow: 0 0 0 3px rgba(44, 92, 77, 0.1);
  outline: none;
}

/* 性别切换开关 */
.gender-toggle {
  position: relative;
  display: flex;
  background: #f0f0f0;
  border-radius: 10px;
  padding: 4px;
  height: 44px; /* Matches input height roughly */
  cursor: pointer;
}
.toggle-track {
  position: absolute;
  top: 4px; left: 4px;
  width: calc(50% - 4px);
  height: calc(100% - 8px);
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: transform 0.3s cubic-bezier(0.4, 0.0, 0.2, 1);
}
.toggle-track.right { transform: translateX(100%); }

.toggle-option {
  flex: 1;
  display: flex; justify-content: center; align-items: center;
  z-index: 1;
  font-size: 14px;
  color: #666;
  font-weight: 600;
  transition: color 0.3s;
}
.toggle-option.active { color: #2c5c4d; }

.start-btn {
  width: 100%;
  margin-top: 10px;
  padding: 14px;
  background: #2c5c4d;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  display: flex; justify-content: center; align-items: center; gap: 8px;
  transition: all 0.3s;
}
.start-btn:hover {
  background: #1e4236;
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(44, 92, 77, 0.2);
}

/* Modal Transition */
.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.4s; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; }

/* ====== 2. 聊天主界面设计 ====== */
.chat-container {
  width: 95%; max-width: 1100px; height: 90vh;
  background: #fff;
  border-radius: 30px;
  box-shadow:
    0 20px 60px rgba(0,0,0,0.05),
    0 0 0 1px rgba(0,0,0,0.02);
  display: flex;
  overflow: hidden;
  z-index: 10;
}

/* 侧边条 */
.side-panel {
  width: 60px;
  background: #1e2623;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 24px;
  color: rgba(255,255,255,0.4);
}
.brand {
  writing-mode: vertical-lr;
  font-size: 18px;
  letter-spacing: 4px;
  font-weight: bold;
  color: #d4af37;
  border-bottom: 1px solid rgba(255,255,255,0.1);
  padding-bottom: 20px;
}

/* 主聊天窗口 */
.chat-main-window {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #fff;
}

/* Header */
.chat-header {
  height: 80px;
  padding: 0 30px;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255,255,255,0.8);
  backdrop-filter: blur(10px);
}

.ai-profile { display: flex; align-items: center; gap: 15px; }
.avatar-ring {
  width: 48px; height: 48px;
  border-radius: 50%;
  padding: 2px;
  border: 2px solid #6fbf9a;
}
.avatar-ring img { width: 100%; height: 100%; border-radius: 50%; background: #f0f4f3; }

.ai-meta h3 { margin: 0; font-size: 16px; color: #222; }
.status-badge {
  display: flex; align-items: center; gap: 6px;
  font-size: 12px; color: #6fbf9a; font-weight: 500; margin-top: 2px;
}
.status-badge .dot { width: 6px; height: 6px; background: #6fbf9a; border-radius: 50%; animation: pulse 2s infinite; }

.action-btn {
  background: none; border: none; font-size: 20px; color: #999;
  cursor: pointer; padding: 8px; transition: 0.3s; border-radius: 50%;
}
.action-btn:hover { background: #f5f5f5; color: #333; }

/* Message Area */
.message-area {
  flex: 1;
  padding: 30px;
  overflow-y: auto;
  background: #fcfdfd;
  display: flex; flex-direction: column; gap: 24px;
}
/* 滚动条美化 */
.message-area::-webkit-scrollbar { width: 6px; }
.message-area::-webkit-scrollbar-thumb { background: #e0e0e0; border-radius: 3px; }

.session-start { text-align: center; margin-bottom: 20px; }
.date-tag {
  background: #f0f2f1; color: #888; font-size: 11px;
  padding: 4px 12px; border-radius: 20px;
}

.message-wrapper {
  display: flex; gap: 16px; max-width: 80%;
  opacity: 0; animation: slideUp 0.3s forwards;
}
.message-wrapper.user { align-self: flex-end; flex-direction: row; justify-content: flex-end; }
.message-wrapper.ai { align-self: flex-start; }

.avatar {
  width: 40px; height: 40px; border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0; font-size: 20px;
}
.ai-avatar { background: #e6f2ed; color: #2c5c4d; }
.user-avatar { background: #fff; border: 1px solid #eee; color: #333; }

.bubble {
  padding: 16px 20px;
  border-radius: 18px;
  font-size: 15px; line-height: 1.6;
  position: relative;
  box-shadow: 0 4px 15px rgba(0,0,0,0.03);
}

.ai-bubble {
  background: #fff; border: 1px solid #f0f0f0; color: #333;
  border-top-left-radius: 4px;
}

.user-bubble {
  background: linear-gradient(135deg, #2c5c4d 0%, #3e7b68 100%);
  color: #fff;
  border-top-right-radius: 4px;
  box-shadow: 0 8px 20px rgba(44, 92, 77, 0.25);
}

/* Typing / Thinking Effect */
.thinking-bubble { display: flex; align-items: center; gap: 10px; }
.thinking-text { font-size: 12px; color: #999; }
.typing-indicator span {
  display: inline-block; width: 6px; height: 6px; background: #6fbf9a;
  border-radius: 50%; margin-right: 4px;
  animation: typing 1.4s infinite ease-in-out both;
}
.typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
.typing-indicator span:nth-child(2) { animation-delay: -0.16s; }

/* Input Footer */
.input-footer {
  padding: 20px 30px;
  background: #fff;
  border-top: 1px solid #f5f5f5;
}

.input-wrapper {
  display: flex; align-items: center;
  background: #f4f6f5;
  border-radius: 16px;
  padding: 8px 8px 8px 20px;
  border: 1px solid transparent;
  transition: all 0.3s;
}
.input-wrapper:focus-within {
  background: #fff;
  border-color: #6fbf9a;
  box-shadow: 0 0 0 4px rgba(111, 191, 154, 0.1);
}

.input-wrapper input {
  flex: 1; border: none; background: transparent; outline: none;
  font-size: 15px; color: #333; font-family: 'Inter', sans-serif;
}

.send-btn {
  width: 44px; height: 44px;
  background: #2c5c4d; color: #fff;
  border: none; border-radius: 12px;
  cursor: pointer; font-size: 18px;
  display: flex; align-items: center; justify-content: center;
  transition: all 0.2s;
}
.send-btn:hover:not(:disabled) { background: #1e4236; transform: scale(1.05); }
.send-btn:disabled { background: #d0d0d0; cursor: not-allowed; }

/* Animations */
@keyframes pulse { 0% { opacity: 0.6; } 50% { opacity: 1; } 100% { opacity: 0.6; } }
@keyframes typing { 0%, 80%, 100% { transform: scale(0); } 40% { transform: scale(1); } }
@keyframes slideUp { from { transform: translateY(10px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }

/* Responsive */
@media (max-width: 768px) {
  .chat-container { width: 100%; height: 100%; border-radius: 0; }
  .side-panel { display: none; }
  .chat-header { padding: 0 15px; }
  .message-wrapper { max-width: 90%; }
}
</style>