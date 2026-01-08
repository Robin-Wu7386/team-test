<template>
  <div class="profile-page" v-if="isLoggedIn">
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
        <h3>我的评论</h3>
        <button class="ghost" @click="fetchMyComments">刷新</button>
      </div>
      <div v-if="loading" class="empty">加载中...</div>
      <div v-else-if="myComments.length === 0" class="empty">暂无评论</div>
      <ul v-else class="comment-list">
        <li v-for="item in myComments" :key="item.id" class="comment-item">
          <div class="time">{{ formatTime(item.created_at) }}</div>
          <p class="content">{{ item.content }}</p>
        </li>
      </ul>
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
const myComments = ref([])

const isLoggedIn = computed(() => userStore.isLoggedIn)
const user = computed(() => userStore.userInfo || {})

const formatTime = (val) => (val ? new Date(val).toLocaleString() : '')

const fetchMyComments = async () => {
  if (!isLoggedIn.value) return
  loading.value = true
  try {
    const res = await axios.get('/api/comments', { params: { userId: user.value.id } })
    if (res.data.success) {
      myComments.value = res.data.data
    } else {
      alert(res.data.msg || '获取评论失败')
    }
  } catch (err) {
    alert('获取评论失败，请稍后重试')
  } finally {
    loading.value = false
  }
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
  fetchMyComments()
})
</script>

<style scoped>
.profile-page {
  max-width: 900px;
  margin: 100px auto 60px;
  padding: 0 20px;
  color: #1a3d2e;
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
}

.section {
  margin-top: 20px;
  background: #fff;
  border-radius: 14px;
  border: 1px solid rgba(0,0,0,0.05);
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
  padding: 18px;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.ghost {
  background: #f5f7f6;
  color: #2d5a47;
  border: 1px solid rgba(0,0,0,0.06);
  padding: 8px 12px;
  border-radius: 10px;
  cursor: pointer;
}

.comment-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.comment-item {
  padding: 12px;
  border-radius: 12px;
  background: #f9fbfa;
  border: 1px solid rgba(0,0,0,0.04);
}

.time {
  font-size: 12px;
  color: #5a8a75;
}

.content {
  margin: 6px 0 0;
  color: #2d5a47;
}

.empty {
  text-align: center;
  padding: 40px 0;
  color: #777;
}
</style>
