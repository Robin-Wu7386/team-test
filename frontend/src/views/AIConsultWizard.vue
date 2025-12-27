<template>
  <div class="main-container">
    <!-- 返回首页按钮 + 页面标题 -->
    <div class="header-wrapper">
      <button @click="goToHome" class="back-home-btn">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M19 12H5M5 12L12 19M5 12L12 5" stroke="#2d5d50" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>返回首页</span>
      </button>

      <div class="page-header">
        <h1>中医体质分析系统</h1>
        <p>填写个人信息和症状，获取专业的体质分析建议</p>
      </div>
    </div>

    <!-- 表单卡片 -->
    <div class="form-card">
      <div class="card-header">
        <h2>个人基础信息</h2>
      </div>
      <div class="form-grid">
        <div class="form-item">
          <label for="age">年龄</label>
          <input
            v-model="age"
            id="age"
            placeholder="请输入您的年龄"
            class="form-input"
            type="number"
          >
        </div>
        <div class="form-item">
          <label for="gender">性别</label>
          <!-- 下拉选择框 -->
          <select
            v-model="gender"
            id="gender"
            class="form-input form-select"
          >
            <option value="">请选择性别</option>
            <option value="男">男</option>
            <option value="女">女</option>
            <option value="其他">其他</option>
          </select>
        </div>
        <div class="form-item">
          <label for="height">身高 (cm)</label>
          <input
            v-model="height"
            id="height"
            placeholder="请输入身高，如：175"
            class="form-input"
            type="number"
          >
        </div>
        <div class="form-item">
          <label for="weight">体重 (kg)</label>
          <input
            v-model="weight"
            id="weight"
            placeholder="请输入体重，如：65"
            class="form-input"
            type="number"
          >
        </div>
      </div>
    </div>

    <!-- 症状描述卡片 -->
    <div class="form-card">
      <div class="card-header">
        <h2>症状描述</h2>
      </div>
      <div class="form-item full-width">
        <label for="symptom">请详细描述您的身体症状</label>
        <textarea
          v-model="symptom"
          id="symptom"
          placeholder="例如：最近容易疲劳，手脚冰凉，睡眠质量差..."
          class="form-textarea"
          rows="5"
        ></textarea>
      </div>
      <button
        @click="submit"
        class="submit-btn"
        :disabled="!symptom.trim()"
      >
        {{ submitting ? '分析中...' : '开始分析' }}
      </button>
    </div>

    <!-- 结果展示卡片 -->
    <div class="form-card result-card" v-if="result">
      <div class="card-header">
        <h2>分析结果</h2>
      </div>
      <div class="result-content">
        <pre>{{ result }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
// 如果使用Vue Router，取消下面注释并确保已配置路由
// import { useRouter } from "vue-router";
// const router = useRouter();

// 响应式数据
const age = ref("");
const gender = ref("");
const height = ref("");
const weight = ref("");
const symptom = ref("");
const result = ref("");
const submitting = ref(false);

// 返回首页函数
const goToHome = () => {
  // 方式1：使用Vue Router跳转（推荐，需提前配置首页路由）
  // router.push('/'); // 替换为你的首页路由路径，如 '/home'

  // 方式2：跳转到指定URL（适合无路由场景）
  window.location.href = '/'; // 替换为你的首页实际URL，如 'index.html'

  // 方式3：仅提示（测试用）
  // alert('返回首页');
};

// 提交函数
function submit() {
  if (!symptom.value.trim()) return;

  submitting.value = true;
  fetch("http://127.0.0.1:5000/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      question: symptom.value,
      age: age.value,
      gender: gender.value,
      height: height.value,
      weight: weight.value
    })
  })
  .then(r => {
    if (!r.ok) throw new Error("请求失败，请检查后端服务是否启动");
    return r.json();
  })
  .then(d => {
    result.value = d.answer;
  })
  .catch(err => {
    result.value = `请求出错：${err.message}`;
    console.error(err);
  })
  .finally(() => {
    submitting.value = false;
  });
}
</script>

<style scoped>
/* 全局样式重置和基础配置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: "Inter", "PingFang SC", "Microsoft YaHei", sans-serif;
}

/* 主容器背景改为森系绿色渐变 */
.main-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background: linear-gradient(180deg, #f0f8f0 0%, #e6f5e6 100%);
  min-height: 100vh;
}

/* 头部包装器：返回按钮 + 标题 */
.header-wrapper {
  display: flex;
  align-items: center;
  margin-bottom: 30px;
}

/* 返回首页按钮样式 */
.back-home-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background-color: #f8fcf8;
  border: 1px solid #e8f0e8;
  border-radius: 8px;
  color: #2d5d50;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-right: 20px;
  white-space: nowrap;
}

.back-home-btn:hover {
  background-color: #e8f5e9;
  border-color: #d0e6d0;
  color: #43786a;
  box-shadow: 0 2px 8px rgba(67, 120, 106, 0.1);
}

.back-home-btn:active {
  transform: scale(0.98);
}

/* 页面标题样式 - 调整颜色为森系绿色 */
.page-header {
  text-align: center;
  padding: 20px 0;
  flex: 1;
}

.page-header h1 {
  color: #2d5d50; /* 森系深绿主色 */
  font-size: 28px;
  margin-bottom: 10px;
  font-weight: 600;
}

.page-header p {
  color: #6b8c82; /* 森系浅绿辅助色 */
  font-size: 16px;
}

/* 卡片通用样式 - 优化阴影和过渡 */
.form-card {
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(67, 120, 106, 0.12);
  padding: 24px;
  margin-bottom: 24px;
  transition: all 0.3s ease;
}

.form-card:hover {
  box-shadow: 0 12px 40px rgba(67, 120, 106, 0.15);
}

/* 卡片标题 - 调整颜色 */
.card-header {
  margin-bottom: 20px;
  border-bottom: 1px solid #e8f0e8; /* 浅绿色分隔线 */
  padding-bottom: 12px;
}

.card-header h2 {
  color: #2d5d50; /* 森系深绿主色 */
  font-size: 20px;
  font-weight: 600;
}

/* 表单网格布局 */
.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

/* 表单项样式 */
.form-item {
  margin-bottom: 16px;
}

.form-item.full-width {
  grid-column: span 2;
  margin-bottom: 20px;
}

.form-item label {
  display: block;
  margin-bottom: 8px;
  color: #43786a; /* 森系绿色标签色 */
  font-size: 14px;
  font-weight: 500;
}

/* 输入框/下拉框通用样式 - 森系绿色主题 */
.form-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e8f0e8; /* 浅绿色边框 */
  border-radius: 12px;
  font-size: 14px;
  transition: all 0.3s ease;
  outline: none;
  background-color: #f8fcf8; /* 浅绿背景 */
  color: #2d5d50;
}

/* 下拉框特殊样式 */
.form-select {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg width='12' height='8' viewBox='0 0 12 8' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M1 1L6 7L11 1' stroke='%2343786a' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 16px center;
  padding-right: 40px;
}

.form-input:focus {
  border-color: #43786a; /* 森系深绿焦点色 */
  box-shadow: 0 0 0 3px rgba(67, 120, 106, 0.1); /* 浅绿色焦点阴影 */
}

.form-input::placeholder {
  color: #99b3aa; /* 浅绿占位符颜色 */
}

/* 文本域样式 */
.form-textarea {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e8f0e8;
  border-radius: 12px;
  font-size: 14px;
  resize: vertical;
  transition: all 0.3s ease;
  outline: none;
  background-color: #f8fcf8;
  color: #2d5d50;
  min-height: 120px;
}

.form-textarea:focus {
  border-color: #43786a;
  box-shadow: 0 0 0 3px rgba(67, 120, 106, 0.1);
}

.form-textarea::placeholder {
  color: #99b3aa;
}

/* 提交按钮样式 - 改为森系绿色渐变 */
.submit-btn {
  width: 100%;
  padding: 14px 0;
  background: linear-gradient(90deg, #43786a 0%, #2d5d50 100%); /* 森系渐变 */
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.submit-btn:not(:disabled):hover {
  background: linear-gradient(90deg, #3a695e 0%, #254e44 100%); /* 加深渐变 */
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(67, 120, 106, 0.2);
}

.submit-btn:not(:disabled):active {
  transform: scale(0.98);
}

.submit-btn:disabled {
  background: #a0b9b2; /* 禁用态浅绿 */
  cursor: not-allowed;
  opacity: 0.8;
}

/* 结果展示区域 - 调整颜色 */
.result-card {
  white-space: pre-wrap;
}

.result-content {
  padding: 20px;
  background-color: #f8fcf8; /* 浅绿背景 */
  border: 1px solid #e8f0e8;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.8;
  color: #2d5d50; /* 深绿文字 */
  max-height: 400px;
  overflow-y: auto;
}

/* 滚动条美化 - 森系风格 */
.result-content::-webkit-scrollbar {
  width: 6px;
}

.result-content::-webkit-scrollbar-track {
  background: #f8fcf8;
}

.result-content::-webkit-scrollbar-thumb {
  background: #d0e6d0;
  border-radius: 3px;
}

.result-content::-webkit-scrollbar-thumb:hover {
  background: #43786a;
}

/* 响应式适配 */
@media (max-width: 768px) {
  .header-wrapper {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .back-home-btn {
    margin-right: 0;
  }

  .page-header {
    text-align: left;
    padding: 0;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .form-item.full-width {
    grid-column: span 1;
  }

  .main-container {
    padding: 16px;
  }

  .page-header h1 {
    font-size: 24px;
  }

  .form-card {
    padding: 20px 16px;
  }
}
</style>