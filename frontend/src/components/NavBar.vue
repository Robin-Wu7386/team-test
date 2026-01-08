<!-- components/NavBar.vue -->
<template>
  <nav class="navbar" :class="{ scrolled: isScrolled }">
    <div class="nav-inner">
<<<<<<< HEAD
      <div class="logo" @click="go('/')">
        <div class="logo-symbol">岐</div>
        <span>岐黄 · 本草智能</span>
      </div>

      <div class="pill-container">
        <div class="pill-menu">
          <RouterLink class="pill-item" to="/">首页</RouterLink>
          <RouterLink class="pill-item" to="/chat_page">智能问诊</RouterLink>
          <RouterLink class="pill-item" to="/ai_consult_wizard">流程问诊</RouterLink>
          <RouterLink class="pill-item" to="/knowledge_graph">知识图谱</RouterLink>
          <RouterLink class="pill-item" to="/recommend">中药推荐</RouterLink>
          <RouterLink class="pill-item" to="/comments">论坛</RouterLink>
        </div>
        <div class="divider"></div>
        <button v-if="!isLoggedIn" class="login-pill" @click="go('/login')">
          <i class="ri-user-3-line"></i>
          <span>登录/注册</span>
        </button>
        <div v-else class="user-chip" @click="toggleMenu">
          <div class="chip-avatar">{{ (currentUser.username || 'U').slice(0, 1).toUpperCase() }}</div>
          <span class="chip-name">{{ currentUser.username }}</span>
          <i class="ri-arrow-down-s-line"></i>
          <div v-if="showMenu" class="chip-menu" @click.stop>
            <button class="chip-action" @click="go('/profile')">个人中心</button>
            <button class="chip-action" @click="goMyComments">我的评论</button>
            <button class="chip-action danger" @click="logout">退出登录</button>
          </div>
        </div>
      </div>
=======
>>>>>>> aef0256c (整合前端)
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const isScrolled = ref(false);
const handleScroll = () => { isScrolled.value = window.scrollY > 50; };
onMounted(() => window.addEventListener('scroll', handleScroll));
onUnmounted(() => window.removeEventListener('scroll', handleScroll));
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0; left: 0; width: 100%;
  z-index: 1000;
  padding: 20px 40px;
  transition: all 0.4s ease;
}

/* 滚动后变窄并增加模糊背景 */
.navbar.scrolled {
  padding: 10px 40px;
  background: rgba(242, 245, 243, 0.8);
  backdrop-filter: blur(16px);
  border-bottom: 1px solid rgba(255,255,255,0.3);
}

.nav-inner {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 20px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  color: var(--primary-dark);
}
.logo-symbol {
  width: 32px; height: 32px;
  background: var(--primary);
  color: white;
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 16px;
  transform: rotate(15deg);
}

.pill-container {
  display: flex;
  align-items: center;
  gap: 15px;
  background: rgba(255,255,255,0.6);
  padding: 6px;
  border-radius: 99px;
  border: 1px solid var(--glass-border);
  box-shadow: 0 4px 20px rgba(0,0,0,0.03);
  backdrop-filter: blur(8px);
}

.pill-menu {
  display: flex;
}

.pill-item {
  text-decoration: none;
  color: var(--text-main);
  font-size: 13px;
  font-weight: 500;
  padding: 8px 20px;
  border-radius: 99px;
  transition: all 0.3s ease;
  position: relative;
}

.pill-item:hover { color: var(--primary); background: rgba(111, 191, 154, 0.1); }
.pill-item.router-link-active {
  background: var(--text-main);
  color: #fff;
  box-shadow: 0 4px 12px rgba(46,74,60,0.3);
}

.divider { width: 1px; height: 16px; background: #ddd; }

.login-pill {
  background: transparent;
  border: none;
  padding: 8px 20px;
  font-size: 13px;
  font-weight: 600;
  color: var(--primary-dark);
  cursor: pointer;
  display: flex; align-items: center; gap: 5px;
  border-radius: 99px;
  transition: all 0.3s;
}
.login-pill:hover { background: #fff; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
</style>