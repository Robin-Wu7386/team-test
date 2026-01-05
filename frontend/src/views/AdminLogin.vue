<template>
  <div class="admin-login-container">
    <div class="login-card">
      <div class="logo">
        <span class="logo-text">中医药智能平台 管理后台</span>
      </div>

      <h2 class="login-title">管理员登录</h2>
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label class="form-label">管理员账号</label>
          <div class="input-wrapper">
            <i class="icon-user">👤</i>
            <input
              v-model="form.username"
              type="text"
              placeholder="请输入管理员账号"
              required
              class="form-input"
            >
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">密码</label>
          <div class="input-wrapper">
            <i class="icon-lock">🔒</i>
            <input
              v-model="form.password"
              type="password"
              placeholder="请输入管理员密码"
              required
              class="form-input"
            >
          </div>
        </div>

        <button type="submit" class="login-btn">登录</button>

        <p class="back-link">
          <router-link to="/login" class="link">返回用户登录</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const form = ref({
  username: '',
  password: ''
})

// 固定账号：admin，密码：admin123，本地校验无需后端接口
const handleLogin = () => {
  // 固定账号密码验证
  const fixedUsername = 'admin'
  const fixedPassword = 'admin123'

  if (form.value.username.trim() !== fixedUsername) {
    alert('管理员账号错误！')
    return
  }

  if (form.value.password !== fixedPassword) {
    alert('管理员密码错误！')
    return
  }

  // 验证通过，存储模拟token（用于路由守卫鉴权）
  localStorage.setItem('adminToken', 'admin_fixed_token_123456')
  alert('登录成功！')
  router.push('/admin/backend') // 跳转到管理后台
}
</script>
<style scoped>
.admin-login-container {
  width: 100%;
  height: 100vh;
  background-color: #f9f5f0;
  background-image: url('data:image/svg+xml;utf8,<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><path d="M30 10Q40 0 50 10Q60 20 50 30Q40 40 30 30Q20 20 30 10Z" fill="%23e8dcc8" opacity="0.3"/><path d="M70 60Q80 50 90 60Q100 70 90 80Q80 90 70 80Q60 70 70 60Z" fill="%23e8dcc8" opacity="0.3"/></svg>');
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-card {
  width: 350px;
  padding: 40px 30px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  border: 1px solid #e8dcc8;
}

.logo {
  text-align: center;
  margin-bottom: 30px;
}

.logo-text {
  font-size: 24px;
  font-weight: bold;
  color: #2d7d46;
  letter-spacing: 2px;
}

.login-title {
  text-align: center;
  color: #2d7d46;
  margin-bottom: 30px;
  font-weight: 600;
  position: relative;
}

.login-title::after {
  content: '';
  display: block;
  width: 50px;
  height: 3px;
  background: #5fb378;
  margin: 10px auto 0;
  border-radius: 3px;
}

.form-group {
  margin-bottom: 25px;
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

.icon-user, .icon-lock {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #4a9c66;
}

/* 按钮样式（匹配图中深绿色） */
.login-btn {
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

.login-btn:hover {
  background: #226338;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.back-link {
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
