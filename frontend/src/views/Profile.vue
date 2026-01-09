<template>
  <div class="profile-page" v-if="isLoggedIn">
    <!-- 返回主页按钮 -->
    <button class="back-home" @click="router.push('/')">
      <i class="ri-arrow-left-line"></i> 返回主页
    </button>
    
    <div class="profile-card">
      <div class="avatar">{{ (user.username || 'U').slice(0, 1).toUpperCase() }}</div>
      <div class="info">
        <h2>{{ user.username }}</h2>
        <p>手机号：{{ user.phonenumber }}</p>
        <p>邮箱：{{ user.email }}</p>
        <p>用户ID：{{ user.id }}</p>
      </div>
      <button class="logout" @click="handleLogout">退出登录</button>
    </div>

    <div class="section">
      <div class="section-header">
        <h3>个人信息</h3>
        <button class="ghost" @click="handleEditToggle">{{ isEditing ? '取消' : '编辑' }}</button>
      </div>
      
      <div v-if="loading" class="empty">加载中...</div>
      <div v-else>
        <form @submit.prevent="handleSubmit" class="profile-form">
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">年龄</label>
              <input 
                v-model="profile.age" 
                type="number" 
                class="form-input" 
                :disabled="!isEditing"
                placeholder="请输入年龄"
              >
            </div>
            <div class="form-group">
              <label class="form-label">性别</label>
              <select 
                v-model="profile.sex" 
                class="form-input" 
                :disabled="!isEditing"
              >
                <option value="">请选择性别</option>
                <option value="男">男</option>
                <option value="女">女</option>
              </select>
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">身高 (cm)</label>
              <input 
                v-model.number="profile.height" 
                type="number" 
                class="form-input" 
                :disabled="!isEditing"
                placeholder="请输入身高"
              >
            </div>
            <div class="form-group">
              <label class="form-label">体重 (kg)</label>
              <input 
                v-model.number="profile.weight" 
                type="number" 
                step="0.1" 
                class="form-input" 
                :disabled="!isEditing"
                placeholder="请输入体重"
              >
            </div>
          </div>
          
          <div v-if="isEditing" class="form-actions">
            <button type="button" class="btn cancel" @click="handleEditToggle">取消</button>
            <button type="submit" class="btn save">保存</button>
          </div>
        </form>
      </div>
    </div>
  </div>
  <div v-else class="empty">
    未登录，请先 <router-link to="/login">登录</router-link>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useUserStore } from '../stores/user'

const router = useRouter()
const userStore = useUserStore()
const loading = ref(false)
const isEditing = ref(false)

const isLoggedIn = computed(() => userStore.isLoggedIn)
const user = computed(() => userStore.userInfo || {})

// 个人信息数据
const profile = ref({
  age: '',
  sex: '',
  height: '',
  weight: ''
})

// 创建带有Authorization头的axios实例
const axiosInstance = axios.create()

// 请求拦截器，添加Authorization头
axiosInstance.interceptors.request.use(
  (config) => {
    // 从localStorage获取token
    const userInfo = localStorage.getItem('userInfo')
    if (userInfo) {
      try {
        const parsedUser = JSON.parse(userInfo)
        if (parsedUser.token) {
          config.headers.Authorization = `Bearer ${parsedUser.token}`
        }
      } catch (e) {
        console.error('解析用户信息失败:', e)
      }
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 获取个人信息
const fetchProfile = async () => {
  if (!isLoggedIn.value) return
  loading.value = true
  try {
    const res = await axiosInstance.get('/api/profile')
    if (res.data.success) {
      const data = res.data.data
      profile.value = {
        age: data.age || '',
        sex: data.sex || '',
        height: data.height || '',
        weight: data.weight || ''
      }
    }
  } catch (err) {
    console.error('获取个人信息失败:', err)
    // 初始化空数据
    profile.value = {
      age: '',
      sex: '',
      height: '',
      weight: ''
    }
  } finally {
    loading.value = false
  }
}

// 保存个人信息
const handleSubmit = async () => {
  loading.value = true
  try {
    const res = await axiosInstance.post('/api/profile', profile.value)
    if (res.data.success) {
      isEditing.value = false
      alert('个人信息保存成功')
    } else {
      alert('保存失败: ' + res.data.msg)
    }
  } catch (err) {
    console.error('保存个人信息失败:', err)
    alert('保存失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 切换编辑状态
const handleEditToggle = () => {
  isEditing.value = !isEditing.value
}

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}

onMounted(() => {
  if (!isLoggedIn.value) {
    router.push('/login')
    return
  }
  fetchProfile()
})
</script>

<style scoped>
.profile-page {
  max-width: 900px;
  margin: 100px auto 60px;
  padding: 0 20px;
  color: #1a3d2e;
}

.back-home {
  background: #fff;
  border: 1px solid rgba(111, 191, 154, 0.3);
  color: #2c5c4d;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s;
  margin-bottom: 20px;
}

.back-home:hover {
  background: #f0fff5;
  border-color: #6fbf9a;
  box-shadow: 0 4px 12px rgba(111, 191, 154, 0.2);
}

.profile-card {
  display: flex;
  align-items: center;
  gap: 18px;
  background: linear-gradient(135deg, #e8f5ef, #f6fff9);
  border: 1px solid rgba(111, 191, 154, 0.25);
  border-radius: 16px;
  padding: 18px;
  box-shadow: 0 10px 40px rgba(111, 191, 154, 0.15);
}

.avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6fbf9a, #2c5c4d);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: 800;
}

.info h2 {
  margin: 0 0 6px;
}

.info p {
  margin: 2px 0;
  color: #4f6d60;
}

.logout {
  margin-left: auto;
  background: #fff5f5;
  color: #c03434;
  border: 1px solid rgba(192, 52, 52, 0.16);
  padding: 10px 12px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
}

.logout:hover {
  background: #ffeaea;
  border-color: rgba(192, 52, 52, 0.3);
}

.section {
  margin-top: 20px;
  background: #fff;
  border-radius: 14px;
  border: 1px solid rgba(0,0,0,0.05);
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
  padding: 24px;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.ghost {
  background: #f5f7f6;
  color: #2d5a47;
  border: 1px solid rgba(0,0,0,0.06);
  padding: 8px 16px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s;
}

.ghost:hover {
  background: #eaf0ed;
  border-color: rgba(0,0,0,0.12);
}

/* 表单样式 */
.profile-form {
  width: 100%;
}

.form-row {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.form-group {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group.full-width {
  width: 100%;
}

.form-label {
  font-size: 14px;
  font-weight: 500;
  color: #2d5a47;
}

.form-input, .form-textarea {
  padding: 10px 12px;
  border: 1px solid #e0d0c0;
  border-radius: 8px;
  font-size: 15px;
  transition: all 0.3s;
  background-color: #fff;
}

.form-input:focus, .form-textarea:focus {
  outline: none;
  border-color: #5fb378;
  box-shadow: 0 0 0 3px rgba(95, 179, 120, 0.2);
}

.form-input:disabled, .form-textarea:disabled {
  background-color: #f9f9f9;
  border-color: #eaeaea;
  cursor: not-allowed;
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.form-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 24px;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.btn.cancel {
  background: #f5f7f6;
  color: #2d5a47;
  border: 1px solid rgba(0,0,0,0.06);
}

.btn.cancel:hover {
  background: #eaf0ed;
  border-color: rgba(0,0,0,0.12);
}

.btn.save {
  background: #2d7d46;
  color: #fff;
}

.btn.save:hover {
  background: #226338;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.empty {
  text-align: center;
  padding: 40px 0;
  color: #777;
}
</style>
