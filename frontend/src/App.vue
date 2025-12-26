<template>
  <router-view />
</template>

<script setup>
// 不需要任何逻辑
</script>

<style>
/* 从原HTML中复制CSS变量和基础样式 */
:root {
  --bg: #f4f8f2;
  --green: #6fbf9a;
  --yellow: #f3e8a5;
  --text: #2e4a3c;
  --header-bg: #fff;
  --border: #ddebe2;
  --card-bg: #fff;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: "Noto Serif SC", serif;
  background: var(--bg);
  color: var(--text);
  height: 100vh;
  overflow: hidden;
}
</style>