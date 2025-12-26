<template>
  <header>
    <div class="logo">
      中医药智能平台
    </div>
    <div class="nav-menu">
      <button
        class="func-button"
        @click="$router.push('/chat_page')"
      >
        智能问诊
      </button>
      <button
        class="func-button"
        @click="$router.push('/ai_consult_wizard')"
      >
        流程问诊
      </button>
      <button
        class="func-button"
        @click="openModal('中药智能推荐')"
      >
        中药推荐
      </button>
      <button
        class="func-button"
        @click="openModal('知识图谱推演')"
      >
        知识图谱
      </button>
      <button
        class="login-button"
        @click="openModal('登录 / 注册')"
      >
        登录 / 注册
      </button>
    </div>
  </header>

  <section class="hero">
    <img
      v-for="(img, i) in imgs"
      :key="i"
      :src="img"
      :class="{ active: i === current }"
    >
  </section>

  <section class="recommend-section">
    <h2>今日推荐</h2>
    <div class="recommend-cards">
      <div
        class="card"
        v-for="item in cards"
        :key="item.name"
        @click="openModal(item.name)"
      >
        <img :src="item.img">
        <div class="card-content">
          <h3>{{ item.name }}</h3>
          <p>{{ item.desc }}</p>
        </div>
      </div>
    </div>
  </section>

  <div
    class="modal"
    :class="{ active: modal }"
    @click.self="modal = false"
  >
    <div class="modal-box">
      <h3>{{ modalTitle }}</h3>
      <p>此处为功能详情 / 后续页面或接口调用位置。</p>
      <button @click="modal = false">
        关闭
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const modal = ref(false);
const modalTitle = ref("");
const current = ref(0);

const imgs = [
  "/static/pictures/zhongyao1.png",
  "/static/pictures/zhongyao2.png",
  "/static/pictures/zhongyao3.png"
];

const cards = [
  {
    name: "黄芪",
    img: "/static/pictures/huangqi.png",
    desc: "补气固表、增强体力"
  },
  {
    name: "当归",
    img: "/static/pictures/danggui.png",
    desc: "补血活血、调经止痛"
  },
  {
    name: "酸枣仁",
    img: "/static/pictures/suanzaoren.png",
    desc: "养心安神、改善睡眠"
  }
];

function openModal(t) {
  modalTitle.value = t;
  modal.value = true;
}

onMounted(() => {
  setInterval(() => {
    current.value = (current.value + 1) % imgs.length;
  }, 4000);
});
</script>

<style scoped>
:root {
  --bg: #f4f8f2;
  --green: #6fbf9a;
  --yellow: #f3e8a5;
  --text: #2e4a3c;
  --border: #ddebe2;
}

header {
  display: flex;
  justify-content: space-between;
  padding: 20px 40px;
  background: #fff;
}

.logo {
  font-size: 22px;
  font-weight: 700;
  color: var(--yellow);
}

.nav-menu {
  display: flex;
  gap: 12px;
}

.func-button,
.login-button {
  padding: 10px 20px;
  border-radius: 20px;
  border: 1px solid var(--border);
}

.hero {
  height: 400px;
  overflow: hidden;
}

.hero img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: none;
}

.hero img.active {
  display: block;
}

.recommend-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.card {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
}

.card img {
  width: 100%;
  height: 160px;
  object-fit: cover;
}

.modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: none;
}

.modal.active {
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-box {
  background: #fff;
  padding: 30px;
  border-radius: 20px;
}
</style>