<template>
  <div class="register-container">
    <h2>用户注册</h2>
    <form @submit.prevent="handleRegister">
      <div>
        <label>用户名</label>
        <input
          v-model="form.username"
          type="text"
          placeholder="请输入用户名"
          required
        >
      </div>
      <div>
        <label>手机号</label>
        <input
          v-model="form.phonenumber"
          type="tel"
          placeholder="请输入手机号"
          required
        >
      </div>
      <div>
        <label>邮箱</label>
        <input
          v-model="form.email"
          type="email"
          placeholder="请输入邮箱"
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
      <div>
        <label>确认密码</label>
        <input
          v-model="form.confirmPwd"
          type="password"
          placeholder="请再次输入密码"
          required
        >
      </div>
      <button type="submit" :disabled="form.password !== form.confirmPwd">注册</button>
      <p>已有账号？<router-link to="/login">去登录</router-link></p>
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

// 注册请求；
const handleRegister = async () => {
  if (form.value.password !== form.value.confirmPwd) {
    alert('两次密码不一致')
    return
  }
  try {
    const res = await axios.post('/api/register', {
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
.register-container {
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