<template>
  <div class="register-container">
    <!-- 中医主题Logo -->
    <div class="logo">
      <span class="logo-text">中医药智能平台</span>
      <p class="logo-desc">本草智能 · 悬壶济世</p>
    </div>

    <h2 class="register-title">用户注册</h2>
    <form @submit.prevent="handleRegister" class="register-form">
      <div class="form-group">
        <label class="form-label">用户名</label>
        <div class="input-wrapper">
          <li class="icon-user">👤</li>
          <input
            v-model="form.username"
            type="text"
            placeholder="请输入用户名"
            required
            class="form-input"
          >
        </div>
      </div>

      <div class="form-group">
        <label class="form-label">手机号</label>
        <div class="input-wrapper">
          <li class="icon-phone">📱</li>
          <input
            v-model="form.phonenumber"
            type="tel"
            placeholder="请输入手机号"
            required
            class="form-input"
          >
        </div>
      </div>

      <div class="form-group">
        <label class="form-label">邮箱</label>
        <div class="input-wrapper">
          <li class="icon-email">📧</li>
          <input
            v-model="form.email"
            type="email"
            placeholder="请输入邮箱"
            required
            class="form-input"
          >
        </div>
      </div>

      <div class="form-group">
        <label class="form-label">密码</label>
        <div class="input-wrapper">
          <li class="icon-lock">🔒</li>
          <input
            v-model="form.password"
            type="password"
            placeholder="请输入6-16位密码"
            required
            class="form-input"
          >
        </div>
      </div>

      <div class="form-group">
        <label class="form-label">确认密码</label>
        <div class="input-wrapper">
          <li class="icon-lock">🔒</li>
          <input
            v-model="form.confirmPwd"
            type="password"
            placeholder="请再次输入密码"
            required
            class="form-input"
          >
        </div>
        <span v-if="form.password && form.confirmPwd && form.password !== form.confirmPwd" class="error-text">
          两次密码不一致
        </span>
      </div>

      <button
        type="submit"
        class="register-btn"
        :disabled="form.password !== form.confirmPwd || !form.password"
      >
        注册
      </button>

      <p class="login-link">
        已有账号？<router-link to="/login" class="link">去登录</router-link>
      </p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const form = ref({
  username: '',
  phonenumber: '',
  email: '',
  password: '',
  confirmPwd: ''
})

const handleRegister = async () => {
  if (form.value.password !== form.value.confirmPwd) {
    alert('两次密码不一致')
    return
  }

  try {
    const res = await axios.post('/api/user/register', {
      username: form.value.username,
      phonenumber: form.value.phonenumber,
      email: form.value.email,
      password: form.value.password
    })

    if (res.data.success) {
      alert('注册成功！请登录')
      router.push('/login')
    } else {
      alert(res.data.msg)
    }
  } catch (err) {
    alert('注册失败，请重试')
  }
}
</script>

<style scoped>
/* 基础样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Microsoft YaHei', sans-serif;
}

body {
  background-color: #f9f5f0;
  background-image: url('data:image/svg+xml;utf8,<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><path d="M30 10Q40 0 50 10Q60 20 50 30Q40 40 30 30Q20 20 30 10Z" fill="%23e8dcc8" opacity="0.3"/><path d="M70 60Q80 50 90 60Q100 70 90 80Q80 90 70 80Q60 70 70 60Z" fill="%23e8dcc8" opacity="0.3"/></svg>');
}

.register-container {
  width: 380px;
  margin: 60px auto;
  padding: 30px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid #e8dcc8;
}

/* Logo样式 */
.logo {
  text-align: center;
  margin-bottom: 25px;
}

.logo-text {
  font-size: 28px;
  font-weight: bold;
  color: #2d7d46;
  letter-spacing: 2px;
}

.logo-desc {
  font-size: 14px;
  color: #4a9c66;
  margin-top: 5px;
}

/* 表单样式 */
.register-title {
  text-align: center;
  color: #2d7d46;
  margin-bottom: 25px;
  font-weight: 600;
  position: relative;
}

.register-title::after {
  content: '';
  display: block;
  width: 50px;
  height: 3px;
  background: #5fb378;
  margin: 10px auto 0;
  border-radius: 3px;
}

.form-group {
  margin-bottom: 18px;
  position: relative;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  color: #2d7d46;
  font-size: 14px;
}

.input-wrapper {
  position: relative;
}

.form-input {
  width: 100%;
  padding: 12px 15px 12px 40px;
  border: 1px solid #e0d0c0;
  border-radius: 8px;
  font-size: 15px;
  transition: all 0.3s;
}

.form-input:focus {
  outline: none;
  border-color: #5fb378;
  box-shadow: 0 0 0 3px rgba(95, 179, 120, 0.2);
}

.icon-user, .icon-phone, .icon-email, .icon-lock {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #4a9c66;
}

.error-text {
  display: block;
  margin-top: 5px;
  font-size: 12px;
  color: #e53e3e;
}

/* 按钮样式（匹配图中深绿色） */
.register-btn {
  width: 100%;
  padding: 13px;
  background: #2d7d46;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  margin-bottom: 20px;
}

.register-btn:disabled {
  background: #5fb378;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.register-btn:not(:disabled):hover {
  background: #226338;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* 链接样式 */
.login-link {
  text-align: center;
  font-size: 14px;
}

.link {
  color: #2d7d46;
  text-decoration: none;
  transition: color 0.3s;
}

.link:hover {
  color: #226338;
  text-decoration: underline;
}
</style>