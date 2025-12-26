<template>
  <div class="wizard-page">
    <div class="wizard-container">

      <!-- ===== 顶部进度条 ===== -->
      <div class="step-header">
        <div
          v-for="(s, i) in steps"
          :key="i"
          class="step-item"
          :class="{ active: step === i }"
        >
          <div class="step-circle">{{ i + 1 }}</div>
          <div class="step-title">{{ s }}</div>
        </div>
      </div>

      <!-- ===== Step 1：基本信息 ===== -->
      <transition name="fade-slide" mode="out-in">
        <div v-if="step === 0" key="step1" class="card">
          <h2>🩺 基本信息采集</h2>
          <p class="desc">用于辅助中医辨证，请如实填写</p>

          <div class="form-grid">
            <div class="input-group">
              <label>年龄</label>
              <input type="number" v-model="age" placeholder="例如：30" />
            </div>

            <div class="input-group">
              <label>性别</label>
              <div class="gender-selector">
                <div
                  class="gender-card"
                  :class="{ active: gender === '男' }"
                  @click="gender = '男'"
                >
                  👨🏻 男
                </div>
                <div
                  class="gender-card"
                  :class="{ active: gender === '女' }"
                  @click="gender = '女'"
                >
                  👩🏻 女
                </div>
              </div>
            </div>

            <div class="input-group">
              <label>身高 (cm)</label>
              <input type="number" v-model="height" />
            </div>

            <div class="input-group">
              <label>体重 (kg)</label>
              <input type="number" v-model="weight" />
            </div>
          </div>

          <div class="actions">
            <button class="primary" @click="nextStep">
              下一步
            </button>
          </div>
        </div>

        <!-- ===== Step 2：症状描述 ===== -->
        <div v-else-if="step === 1" key="step2" class="card">
          <h2>📋 症状与主诉</h2>
          <p class="desc">
            请详细描述不适症状、持续时间、加重或缓解因素
          </p>

          <textarea
            v-model="symptom"
            placeholder="例如：近两周失眠多梦，伴随乏力、口干，夜间加重..."
          ></textarea>

          <div class="actions">
            <button class="ghost" @click="step--">上一步</button>
            <button class="primary" @click="nextStep">
              开始分析
            </button>
          </div>
        </div>

        <!-- ===== Step 3：AI 结果 ===== -->
        <div v-else key="step3" class="card">
          <h2>🧠 AI 辨证分析结果</h2>

          <div v-if="loading" class="loading">
            🌿 正在进行中医辨证分析…
          </div>

          <div v-else class="result-card">
            <pre>{{ result }}</pre>
          </div>

          <div class="actions">
            <button class="ghost" @click="restart">
              重新问诊
            </button>
          </div>
        </div>
      </transition>

    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

/* ===== 步骤 ===== */
const steps = ["基本信息", "症状描述", "AI分析"];
const step = ref(0);

/* ===== 表单数据 ===== */
const age = ref("");
const gender = ref("");
const height = ref("");
const weight = ref("");
const symptom = ref("");

/* ===== 结果 ===== */
const result = ref("");
const loading = ref(false);

function nextStep() {
  if (step.value === 0) {
    if (!age.value || !gender.value) {
      alert("请填写年龄并选择性别");
      return;
    }
    step.value++;
  } else if (step.value === 1) {
    if (!symptom.value) {
      alert("请填写症状描述");
      return;
    }
    step.value++;
    submit();
  }
}

function restart() {
  step.value = 0;
  symptom.value = "";
  result.value = "";
}

/* ===== 原有接口，不动 ===== */
function submit() {
  loading.value = true;

  fetch("http://127.0.0.1:5000/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      question: symptom.value,
      profile: {
        age: age.value,
        gender: gender.value,
        height: height.value,
        weight: weight.value
      }
    })
  })
    .then(r => r.json())
    .then(d => {
      result.value = d.answer;
      loading.value = false;
    })
    .catch(() => {
      result.value = "分析失败，请稍后再试。";
      loading.value = false;
    });
}
</script>

<style scoped>
.wizard-page {
  min-height: 100vh;
  background: #f5f7fa;
  display: flex;
  justify-content: center;
  padding: 40px 20px;
}

/* 容器 */
.wizard-container {
  width: 100%;
  max-width: 900px;
}

/* ===== 顶部步骤 ===== */
.step-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30px;
}

.step-item {
  flex: 1;
  text-align: center;
  color: #a0aec0;
}

.step-item.active {
  color: var(--primary, #42b983);
}

.step-circle {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #e2e8f0;
  margin: 0 auto 8px;
  line-height: 36px;
  font-weight: 700;
}

.step-item.active .step-circle {
  background: var(--primary, #42b983);
  color: #fff;
}

.step-title {
  font-size: 0.85rem;
}

/* ===== 卡片 ===== */
.card {
  background: #fff;
  border-radius: 24px;
  padding: 36px;
  box-shadow: 0 20px 40px rgba(0,0,0,.06);
}

.desc {
  color: #718096;
  margin: 8px 0 24px;
}

/* 表单 */
.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.input-group label {
  font-size: 0.85rem;
  font-weight: 600;
  margin-bottom: 6px;
  display: block;
}

.input-group input {
  width: 100%;
  padding: 12px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

/* 性别 */
.gender-selector {
  display: flex;
  gap: 12px;
}

.gender-card {
  flex: 1;
  padding: 12px;
  border-radius: 14px;
  border: 1px solid #e2e8f0;
  text-align: center;
  cursor: pointer;
  transition: .2s;
}

.gender-card.active {
  background: var(--primary, #42b983);
  color: white;
  border-color: var(--primary, #42b983);
}

/* 症状 */
textarea {
  width: 100%;
  min-height: 160px;
  padding: 16px;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  resize: vertical;
}

/* 结果 */
.result-card {
  background: #f7fafc;
  padding: 20px;
  border-radius: 16px;
  margin-top: 20px;
}

pre {
  white-space: pre-wrap;
  line-height: 1.7;
}

/* 操作按钮 */
.actions {
  margin-top: 30px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.primary {
  background: var(--primary, #42b983);
  color: white;
  border: none;
  border-radius: 20px;
  padding: 10px 28px;
}

.ghost {
  background: transparent;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  padding: 10px 24px;
}

/* 动画 */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}
.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(20px);
}
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>
