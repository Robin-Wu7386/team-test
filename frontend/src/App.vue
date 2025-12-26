<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup>
</script>

<style>
:root {
  --bg: #f4f8f2;
  --primary: #6fbf9a;
  --secondary: #f3e8a5;
  --text: #2e4a3c;
  --border: #ddebe2;
  --card-bg: #ffffff;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: "Noto Serif SC", "PingFang SC", serif;
  background: var(--bg);
  color: var(--text);
}

button {
  cursor: pointer;
  border: none;
  border-radius: 999px;
  padding: 10px 22px;
  background: var(--primary);
  color: #fff;
  font-size: 14px;
  transition: all 0.25s ease;
}

button:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 18px rgba(0,0,0,.15);
}

input,
textarea {
  border-radius: 14px;
  border: 1px solid var(--border);
  padding: 12px 16px;
  font-size: 14px;
  outline: none;
  width: 100%;
}

input:focus,
textarea:focus {
  border-color: var(--primary);
}
</style>
