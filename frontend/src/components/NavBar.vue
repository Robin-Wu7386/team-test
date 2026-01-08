<!-- components/NavBar.vue -->
<template>
  <nav class="navbar" :class="{ scrolled: isScrolled }">
    <div class="nav-inner">
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
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue';
import { useRouter, RouterLink } from 'vue-router';
import { useUserStore } from '../stores/user';

const isScrolled = ref(false);
const showMenu = ref(false);
const router = useRouter();
const userStore = useUserStore();

const handleScroll = () => { isScrolled.value = window.scrollY > 50; };
onMounted(() => window.addEventListener('scroll', handleScroll));
onUnmounted(() => window.removeEventListener('scroll', handleScroll));

const go = (path) => {
  showMenu.value = false;
  router.push(path);
};

const goMyComments = () => {
  showMenu.value = false;
  router.push({ path: '/comments', query: { tab: 'mine' } });
};

const logout = () => {
  userStore.logout();
  showMenu.value = false;
  router.push('/login');
};

const toggleMenu = () => {
  showMenu.value = !showMenu.value;
};

const isLoggedIn = computed(() => userStore.isLoggedIn);
const currentUser = computed(() => userStore.userInfo || {});
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0; left: 0; width: 100%;
  z-index: 1000;
  padding: 16px 30px;
  transition: all 0.4s ease;
}

/* 滚动后变窄并增加模糊背景 */
.navbar.scrolled {
  padding: 10px 30px;
  background: rgba(242, 245, 243, 0.85);
  backdrop-filter: blur(16px);
  border-bottom: 1px solid rgba(255,255,255,0.3);
}

.nav-inner {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: nowrap; /* 强制不换行 */
}

.logo {
  font-size: 18px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  color: var(--primary-dark);
  letter-spacing: 1px;
  white-space: nowrap; /* logo也不换行 */
  flex-shrink: 0; /* 防止logo被压缩 */
}
.logo-symbol {
  width: 32px; height: 32px;
  background: var(--primary);
  color: white;
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 16px;
  transform: rotate(15deg);
  flex-shrink: 0;
}

.pill-container {
  display: flex;
  align-items: center;
  gap: 15px;
  background: rgba(255,255,255,0.7);
  padding: 6px;
  border-radius: 99px;
  border: 1px solid var(--glass-border);
  box-shadow: 0 4px 20px rgba(0,0,0,0.03);
  backdrop-filter: blur(8px);
  flex-wrap: nowrap; /* 强制不换行 */
  flex-shrink: 0; /* 防止容器被压缩太厉害 */
}

.pill-menu {
  display: flex;
  flex-wrap: nowrap; /* 强制不换行 */
}

.pill-item {
  text-decoration: none;
  color: var(--text-main);
  font-size: 13px;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 99px;
  transition: all 0.3s ease;
  position: relative;
  white-space: nowrap;
}

.pill-item:hover { color: var(--primary); background: rgba(111, 191, 154, 0.1); }
.pill-item.router-link-active {
  background: var(--text-main);
  color: #fff;
  box-shadow: 0 4px 12px rgba(46,74,60,0.3);
}

.divider { width: 1px; height: 22px; background: #ddd; }

.login-pill {
  background: transparent;
  border: none;
  padding: 10px 18px;
  font-size: 13px;
  font-weight: 600;
  color: var(--primary-dark);
  cursor: pointer;
  display: flex; align-items: center; gap: 5px;
  border-radius: 99px;
  transition: all 0.3s;
}
.login-pill:hover { background: #fff; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }

.user-chip {
  position: relative;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 999px;
  background: rgba(45, 90, 71, 0.06);
  border: 1px solid rgba(45, 90, 71, 0.14);
  cursor: pointer;
}

.chip-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
}

.chip-name {
  font-size: 13px;
  color: var(--text-main);
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.chip-menu {
  position: absolute;
  top: 42px;
  right: 0;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
  border: 1px solid rgba(0,0,0,0.06);
  padding: 8px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-width: 160px;
  z-index: 1200;
}

.chip-action {
  border: 1px solid rgba(45, 90, 71, 0.12);
  background: #f8fdfa;
  padding: 10px 12px;
  border-radius: 10px;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s;
  color: var(--text-main);
}

.chip-action:hover {
  background: rgba(111, 191, 154, 0.16);
  border-color: var(--primary);
}

.chip-action.danger {
  color: #c03434;
  border-color: rgba(192, 52, 52, 0.16);
  background: #fff7f7;
}

.chip-action.danger:hover {
  background: #ffeaea;
  border-color: #c03434;
}
</style>