<!-- App.vue -->
<template>
  <div id="app">
    <NavBar v-if="!$route.meta.hideNav" />
    <router-view v-slot="{ Component }">
      <transition name="page-fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </div>
</template>

<script setup>
import NavBar from './components/NavBar.vue'
</script>

<style>
/* 引入字体和图标 */
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;500;700&family=Playfair+Display:ital,wght@0,600;1,600&display=swap');
@import url("https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css");

:root {
  --primary: #6fbf9a;
  --primary-dark: #2c5c4d;
  --accent: #d4af37; /* 金色点缀 */
  --bg: #f2f5f3;
  --surface: rgba(255, 255, 255, 0.85);
  --text-main: #2e4a3c;
  --text-sub: #6c8c7c;
  --glass-border: rgba(255, 255, 255, 0.5);
  --shadow-soft: 0 20px 40px rgba(46, 74, 60, 0.05);
  --shadow-hover: 0 30px 60px rgba(46, 74, 60, 0.12);

  /* 新增变量 - 必须的 */
  --green: #1abc9c;        /* 主要绿色，用于按钮、标题 */
  --yellow: #f1c40f;       /* 金色点缀，用于高亮 */
  --border: rgba(0,0,0,0.1); /* 卡片和输入框边框颜色 */
  --card-bg: rgba(255, 255, 255, 0.9); /* 卡片背景 */
  --header-bg: linear-gradient(135deg, #6fbf9a, #2c5c4d); /* 可以改成你喜欢的渐变或纯色 */

}


* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: "Noto Serif SC", serif;
  background-color: var(--bg);
  color: var(--text-main);
  overflow-x: hidden;
  -webkit-font-smoothing: antialiased;
}

/* 页面切换动画 */
.page-fade-enter-active, .page-fade-leave-active {
  transition: opacity 0.6s cubic-bezier(0.25, 0.8, 0.25, 1), transform 0.6s ease;
}
.page-fade-enter-from { opacity: 0; transform: translateY(20px); }
.page-fade-leave-to { opacity: 0; transform: translateY(-20px); }

/* 滚动条美化 */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--primary); border-radius: 4px; }
</style>