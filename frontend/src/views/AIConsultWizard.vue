<template>
  <div class="wizard-page">
    <div class="wizard-content">

      <!-- 进度指示器 -->
      <div class="stepper">
        <div
          v-for="(s, i) in steps"
          :key="i"
          class="step-wrapper"
          :class="{ active: step >= i, current: step === i }"
        >
          <div class="step-circle">{{ i + 1 }}</div>
          <span class="step-label">{{ s }}</span>
          <div class="step-line" v-if="i < steps.length - 1"></div>
        </div>
      </div>

      <!-- 主卡片区域 -->
      <div class="main-card-frame">
        <transition name="card-slide" mode="out-in">

          <!-- Step 1 -->
          <div v-if="step === 0" key="step1" class="step-panel">
            <div class="panel-header">
              <h2>基本信息</h2>
              <p>请如实填写，以便 AI 进行体质辨识</p>
            </div>

            <div class="grid-form">
              <div class="form-item">
                <label>年龄</label>
                <input type="number" v-model="age" class="clean-input" placeholder="Age" />
              </div>
              <div class="form-item">
                <label>性别</label>
                <div class="sex-select">
                  <div class="sex-opt" :class="{selected: gender==='男'}" @click="gender='男'">男</div>
                  <div class="sex-opt" :class="{selected: gender==='女'}" @click="gender='女'">女</div>
                </div>
              </div>
              <div class="form-item"><label>身高 (cm)</label><input type="number" v-model="height" class="clean-input" /></div>
              <div class="form-item"><label>体重 (kg)</label><input type="number" v-model="weight" class="clean-input" /></div>
            </div>

            <div class="panel-footer">
              <button class="next-btn" @click="nextStep">下一步 <i class="arrow">→</i></button>
            </div>
          </div>

          <!-- Step 2 -->
          <div v-else-if="step === 1" key="step2" class="step-panel">
            <div class="panel-header">
              <h2>症状主诉</h2>
              <p>请详细描述您的不适感受</p>
            </div>

            <div class="textarea-wrapper">
              <textarea
                v-model="symptom"
                placeholder="例如：入睡困难，多梦易醒，伴有心悸..."
              ></textarea>
            </div>

            <div class="panel-footer space-between">
              <button class="back-btn" @click="step--">返回</button>
              <button class="next-btn" @click="nextStep">开始辨证</button>
            </div>
          </div>

          <!-- Step 3 -->
          <div v-else key="step3" class="step-panel result-panel">
            <div class="panel-header center">
              <h2>AI 辨证报告</h2>
            </div>

            <div v-if="loading" class="loading-state">
              <div class="spinner"></div>
              <p>正在分析脉络与病机...</p>
            </div>

            <div v-else class="result-paper">
              <div class="paper-texture"></div>
              <pre>{{ result }}</pre>
            </div>

            <div class="panel-footer center">
              <button class="back-btn outline" @click="restart">重新问诊</button>
            </div>
          </div>

        </transition>
      </div>
    </div>
  </div>
</template>

<script setup>
// ----- 逻辑保持不变 -----
import { ref } from "vue";

const steps = ["基础档案", "症状描述", "辨证结果"];
const step = ref(0);
const age = ref("");
const gender = ref("");
const height = ref("");
const weight = ref("");
const symptom = ref("");
const result = ref("");
const loading = ref(false);

function nextStep() {
  if (step.value === 0) {
    if (!age.value || !gender.value) { alert("请填写年龄并选择性别"); return; }
    step.value++;
  } else if (step.value === 1) {
    if (!symptom.value) { alert("请填写症状描述"); return; }
    step.value++;
    submit();
  }
}

function restart() {
  step.value = 0; symptom.value = ""; result.value = "";
}

function submit() {
  loading.value = true;
  fetch("http://127.0.0.1:5000/ask", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question: symptom.value, profile: { age: age.value, gender: gender.value, height: height.value, weight: weight.value } })
  }).then(r => r.json()).then(d => { result.value = d.answer; loading.value = false; })
    .catch(() => { result.value = "分析失败，请稍后再试。"; loading.value = false; });
}
</script>

<style scoped>
.wizard-page {
  min-height: 100vh;
  background: #f4f8f2;
  display: flex; justify-content: center; align-items: center;
  font-family: "Noto Serif SC", serif;
}

.wizard-content { width: 100%; max-width: 700px; padding: 20px; }

/* Stepper */
.stepper { display: flex; justify-content: space-between; margin-bottom: 40px; position: relative; }
.step-wrapper { flex: 1; display: flex; flex-direction: column; align-items: center; position: relative; z-index: 1; }
.step-circle {
  width: 40px; height: 40px; border-radius: 50%; background: #e0e7e3; color: #888;
  display: flex; align-items: center; justify-content: center; font-weight: 700; transition: 0.3s;
  border: 2px solid #fff;
}
.step-label { font-size: 13px; margin-top: 8px; color: #999; transition: 0.3s; }
.step-line {
  position: absolute; top: 20px; left: 50%; width: 100%; height: 2px; background: #e0e7e3; z-index: -1;
}

.step-wrapper.active .step-circle { background: #6fbf9a; color: white; border-color: #6fbf9a; }
.step-wrapper.active .step-label { color: #2c5c4d; font-weight: 600; }
.step-wrapper.active .step-line { background: #6fbf9a; }

/* Main Card */
.main-card-frame {
  background: #fff; border-radius: 24px; box-shadow: 0 20px 60px rgba(46,74,60,0.08);
  overflow: hidden; min-height: 450px; position: relative;
}

.step-panel { padding: 40px 50px; }
.panel-header h2 { font-size: 24px; color: #2c5c4d; margin-bottom: 5px; }
.panel-header p { color: #888; font-size: 14px; margin-bottom: 30px; }
.panel-header.center { text-align: center; }

.grid-form { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.form-item label { display: block; font-size: 12px; font-weight: 600; color: #666; margin-bottom: 8px; }
.clean-input {
  width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-family: inherit;
  transition: 0.3s; background: #fbfdfc;
}
.clean-input:focus { border-color: #6fbf9a; background: white; outline: none; }

.sex-select { display: flex; gap: 10px; }
.sex-opt {
  flex: 1; padding: 10px; text-align: center; border: 1px solid #ddd; border-radius: 8px; cursor: pointer;
}
.sex-opt.selected { background: #6fbf9a; color: white; border-color: #6fbf9a; }

.textarea-wrapper textarea {
  width: 100%; height: 200px; padding: 15px; border: 1px solid #ddd; border-radius: 12px;
  background: #fbfdfc; font-family: inherit; font-size: 15px; resize: none;
}
.textarea-wrapper textarea:focus { border-color: #6fbf9a; outline: none; }

.panel-footer { margin-top: 40px; display: flex; justify-content: flex-end; }
.panel-footer.space-between { justify-content: space-between; }
.panel-footer.center { justify-content: center; }

.next-btn {
  background: #2c5c4d; color: white; padding: 12px 30px; border-radius: 99px; border: none;
  font-size: 15px; cursor: pointer; transition: 0.3s;
}
.next-btn:hover { background: #1e4236; transform: translateY(-2px); }
.back-btn { background: transparent; border: none; color: #666; cursor: pointer; padding: 10px 20px; }
.back-btn.outline { border: 1px solid #ddd; border-radius: 99px; }

/* Result Paper */
.result-paper {
  background: #fefdf5; padding: 30px; border-radius: 4px; border: 1px solid #eaddcf;
  position: relative; margin-top: 20px; box-shadow: 0 5px 15px rgba(0,0,0,0.05);
}
.result-paper pre { white-space: pre-wrap; color: #2e4a3c; line-height: 1.8; font-family: "Noto Serif SC", serif; }

.loading-state { text-align: center; padding: 50px; color: #666; }
.spinner {
  width: 40px; height: 40px; border: 3px solid #eee; border-top-color: #6fbf9a;
  border-radius: 50%; margin: 0 auto 20px; animation: spin 1s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }
.card-slide-enter-active, .card-slide-leave-active { transition: all 0.4s ease; }
.card-slide-enter-from { opacity: 0; transform: translateX(30px); }
.card-slide-leave-to { opacity: 0; transform: translateX(-30px); }
</style>