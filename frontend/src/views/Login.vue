<template>
  <div class="login-container">
    <h2>用户登录</h2>
    <form @submit.prevent="handleLogin">
      <div>
        <label>用户名/手机号</label>
        <input
          v-model="form.account"
          type="text"
          placeholder="请输入用户名或手机号"
          required
        >
      </div>
      <div>
        <label>密码</label>
        <input
          v-model="form.password"
          type="password"
          placeholder="请输入密码"
          required
        >
      </div>
      <button type="submit">登录</button>
      <p>没有账号？<router-link to="/register">去注册</router-link></p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios' // 需先安装：npm install axios

const router = useRouter()
const form = ref({
  account: '',
  password: ''
})

// 登录请求；
const handleLogin = async () => {
  try {
    const res = await axios.post('/api/login', form.value)
    if (res.data.success) {
      // 登录成功：存储token/用户信息，跳转到首页
      localStorage.setItem('userInfo', JSON.stringify(res.data.data))
      router.push('/')
    } else {
      alert(res.data.msg)
    }
  } catch (err) {
    alert('登录失败，请重试')
  }
}
</script>

<style scoped>
.login-container {
  width: 300px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #eee;
}
form div {
  margin-bottom: 15px;
}
input {
  width: 100%;
  padding: 8px;
}
</style>