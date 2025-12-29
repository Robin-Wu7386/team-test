<template>
  <div class="herbal-archive">
    <!-- 背景层系统 -->
    <div class="bg-layer paper-texture"></div>
    <div class="bg-layer ink-blobs">
      <div class="blob blob-green-1"></div>
      <div class="blob blob-gold-1"></div>
    </div>
    <div class="bg-layer floating-particles">
      <div v-for="n in 30" :key="n" class="particle" :style="getParticleStyle(n)"></div>
    </div>

    <!-- 顶部控制区 -->
    <div class="archive-header">
      <div class="header-left">
        <button class="back-btn" @click="$router.push('/')">
          <i class="ri-arrow-left-line"></i>
          <span>返回</span>
        </button>
        <div class="title-group">
          <h1 class="page-title">
            <span class="title-main">本草</span>
            <span class="title-divider">·</span>
            <span class="title-sub">图鉴</span>
          </h1>
          <p class="title-desc">Traditional Chinese Medicine Archive</p>
        </div>
      </div>

      <!-- 搜索框 -->
      <div class="search-bar">
        <i class="ri-search-2-line search-icon"></i>
        <input
          type="text"
          v-model="searchQuery"
          placeholder="搜索本草（如：人参、甘草）..."
          @focus="searchFocused = true"
          @blur="searchFocused = false"
        />
        <div class="search-glow" :class="{ active: searchFocused }"></div>
      </div>
    </div>

    <!-- 过滤器 -->
    <div class="filter-bar">
      <div class="filter-label">
        <i class="ri-filter-3-line"></i>
        <span>分类筛选</span>
      </div>
      <div class="filter-tags">
        <div
          v-for="cat in categories"
          :key="cat"
          class="filter-tag"
          :class="{ active: currentCategory === cat }"
          @click="currentCategory = cat"
        >
          <span class="tag-text">{{ cat }}</span>
          <div class="tag-underline"></div>
        </div>
      </div>
    </div>

    <!-- 药材展示网格 -->
    <div class="herbs-container">
      <transition-group name="list-anim" tag="div" class="herbs-grid">
        <div
          v-for="herb in filteredHerbs"
          :key="herb.id"
          class="herb-card"
          @click="showDetail(herb)"
          @mouseenter="hoveredCard = herb.id"
          @mouseleave="hoveredCard = null"
        >
          <!-- 卡片背景装饰 -->
          <div class="card-bg-decoration"></div>
          <div class="card-bg-text">{{ herb.pinyin }}</div>

          <!-- 药材图标区域 -->
          <div class="herb-visual-wrapper">
            <div class="herb-visual" :style="{ backgroundColor: herb.color }">
              <span class="herb-char">{{ herb.name.charAt(0) }}</span>
              <div class="herb-glow"></div>
            </div>
            <div class="herb-category-badge">{{ herb.category }}</div>
          </div>

          <!-- 内容区域 -->
          <div class="herb-content">
            <h3 class="herb-name">{{ herb.name }}</h3>
            <div class="herb-pinyin">{{ herb.pinyin }}</div>

            <div class="herb-tags">
              <span class="tag nature">
                <i class="ri-fire-line"></i>
                <span>{{ herb.nature }}</span>
              </span>
              <span class="tag flavor">
                <i class="ri-drop-line"></i>
                <span>{{ herb.flavor }}</span>
              </span>
            </div>

            <p class="herb-summary">{{ herb.summary }}</p>
          </div>

          <!-- 卡片底部 -->
          <div class="card-footer">
            <span class="footer-text">查看详情</span>
            <i class="ri-arrow-right-line footer-icon"></i>
            <div class="footer-line"></div>
          </div>

          <!-- 悬浮光效 -->
          <div class="card-hover-glow" v-if="hoveredCard === herb.id"></div>
        </div>
      </transition-group>

      <!-- 无结果提示 -->
      <transition name="fade">
        <div v-if="filteredHerbs.length === 0" class="no-result">
          <div class="no-result-icon">
            <i class="ri-leaf-line"></i>
          </div>
          <h3>未找到相关本草</h3>
          <p>试试其他关键词或分类</p>
        </div>
      </transition>
    </div>

    <!-- 详情弹窗 (精美书页效果) -->
    <transition name="modal-pop">
      <div v-if="selectedHerb" class="detail-overlay" @click.self="selectedHerb = null">
        <div class="detail-book" @click.stop>
          <!-- 关闭按钮 -->
          <button class="close-btn" @click="selectedHerb = null">
            <i class="ri-close-line"></i>
          </button>

          <!-- 书页左侧 -->
          <div class="book-left">
            <div class="book-page-decoration"></div>
            <div class="big-visual-wrapper">
              <div class="big-visual" :style="{ backgroundColor: selectedHerb.color }">
                <span class="big-char">{{ selectedHerb.name }}</span>
                <div class="visual-rings">
                  <div class="ring ring-1"></div>
                  <div class="ring ring-2"></div>
                </div>
              </div>
              <div class="visual-label">本草图鉴</div>
            </div>

            <!-- 归经信息 -->
            <div class="meridians-section">
              <div class="section-title">
                <i class="ri-map-pin-line"></i>
                <span>归经</span>
              </div>
              <div class="meridian-list">
                <span
                  v-for="(m, index) in selectedHerb.meridians"
                  :key="m"
                  class="meridian-item"
                  :style="{ animationDelay: `${index * 0.1}s` }"
                >
                  {{ m }}
                </span>
              </div>
            </div>

            <!-- 分类标签 -->
            <div class="category-display">
              <span class="category-tag-large">{{ selectedHerb.category }}</span>
            </div>
          </div>

          <!-- 书页右侧 -->
          <div class="book-right">
            <div class="book-content">
              <!-- 标题 -->
              <div class="book-header">
                <h2 class="herb-title-main">{{ selectedHerb.name }}</h2>
                <p class="herb-title-pinyin">{{ selectedHerb.pinyin }}</p>
              </div>

              <!-- 属性信息 -->
              <div class="properties-grid">
                <div class="prop-item">
                  <div class="prop-icon">
                    <i class="ri-fire-line"></i>
                  </div>
                  <div class="prop-content">
                    <label>性</label>
                    <span>{{ selectedHerb.nature }}</span>
                  </div>
                </div>
                <div class="prop-item">
                  <div class="prop-icon">
                    <i class="ri-drop-line"></i>
                  </div>
                  <div class="prop-content">
                    <label>味</label>
                    <span>{{ selectedHerb.flavor }}</span>
                  </div>
                </div>
              </div>

              <!-- 功效主治 -->
              <div class="section">
                <div class="section-header">
                  <i class="ri-magic-line section-icon"></i>
                  <h3>功效主治</h3>
                </div>
                <div class="section-content">
                  <p>{{ selectedHerb.desc }}</p>
                </div>
              </div>

              <!-- 现代药理 -->
              <div class="section">
                <div class="section-header">
                  <i class="ri-flask-line section-icon"></i>
                  <h3>现代药理</h3>
                </div>
                <div class="section-content">
                  <p>{{ selectedHerb.modern }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- 书页中缝装饰 -->
          <div class="book-spine"></div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const searchQuery = ref('');
const currentCategory = ref('全部');
const selectedHerb = ref(null);
const searchFocused = ref(false);
const hoveredCard = ref(null);

const categories = ['全部', '解表药', '清热药', '补益药', '理气药', '活血药'];

// 模拟数据
const herbDatabase = [
  {
    id: 1, name: '人参', pinyin: 'Ren Shen', category: '补益药',
    nature: '微温', flavor: '甘、微苦', color: '#e6cbaec0',
    meridians: ['脾', '肺', '心'],
    summary: '大补元气，复脉固脱，补脾益肺。',
    desc: '用于体虚欲脱，肢冷脉微，脾虚食少，肺虚喘咳，津伤口渴，内热消渴，气血亏虚，久病虚羸，惊悸失眠，阳痿宫冷。',
    modern: '具有抗休克、抗疲劳、增强免疫力、调节中枢神经系统等作用。'
  },
  {
    id: 2, name: '柴胡', pinyin: 'Chai Hu', category: '解表药',
    nature: '微寒', flavor: '苦、辛', color: '#8d6e63cc',
    meridians: ['肝', '胆', '肺'],
    summary: '疏肝解郁，升举阳气，退热截疟。',
    desc: '主治感冒发热，寒热往来，胸胁胀痛，月经不调，子宫脱垂，脱肛。',
    modern: '有解热、镇痛、镇静、抗炎、护肝、抗病毒等作用。'
  },
  {
    id: 3, name: '金银花', pinyin: 'Jin Yin Hua', category: '清热药',
    nature: '寒', flavor: '甘', color: '#ffecb3cc',
    meridians: ['肺', '心', '胃'],
    summary: '清热解毒，疏散风热。',
    desc: '用于痈肿疔疮，喉痹，丹毒，热毒血痢，风热感冒，温病发热。',
    modern: '广谱抗菌作用，抗病毒，增强免疫功能，抗炎。'
  },
  {
    id: 4, name: '当归', pinyin: 'Dang Gui', category: '补益药',
    nature: '温', flavor: '甘、辛', color: '#d7ccc8cc',
    meridians: ['肝', '心', '脾'],
    summary: '补血活血，调经止痛，润肠通便。',
    desc: '血虚萎黄，眩晕心悸，月经不调，经闭痛经，虚寒腹痛，风湿痹痛，跌扑损伤，痈疽疮疡，肠燥便秘。',
    modern: '促进造血功能，抑制血小板聚集，降血脂，抗氧化。'
  },
  {
    id: 5, name: '陈皮', pinyin: 'Chen Pi', category: '理气药',
    nature: '温', flavor: '苦、辛', color: '#ffcc80cc',
    meridians: ['脾', '肺'],
    summary: '理气健脾，燥湿化痰。',
    desc: '用于脘腹胀满，食少吐泻，咳嗽痰多。',
    modern: '助消化，祛痰，平喘，扩张冠状动脉。'
  },
  {
    id: 6, name: '丹参', pinyin: 'Dan Shen', category: '活血药',
    nature: '微寒', flavor: '苦', color: '#ef9a9acc',
    meridians: ['心', '肝'],
    summary: '活血祛瘀，通经止痛，清心除烦，凉血消痈。',
    desc: '用于胸痹心痛，脘腹胁痛，症瘕积聚，热痹疼痛，心烦不眠，月经不调，痛经经闭，疮疡肿痛。',
    modern: '扩张冠脉，改善微循环，抗血栓形成。'
  },
];

const filteredHerbs = computed(() => {
  return herbDatabase.filter(herb => {
    const matchesSearch = herb.name.includes(searchQuery.value) ||
                         herb.pinyin.toLowerCase().includes(searchQuery.value.toLowerCase());
    const matchesCat = currentCategory.value === '全部' || herb.category === currentCategory.value;
    return matchesSearch && matchesCat;
  });
});

const showDetail = (herb) => {
  selectedHerb.value = herb;
};

// 粒子样式
const getParticleStyle = (n) => {
  const size = Math.random() * 4 + 2;
  const duration = 20 + Math.random() * 25;
  return {
    left: `${Math.random() * 100}%`,
    top: `${Math.random() * 100}%`,
    width: `${size}px`,
    height: `${size}px`,
    animationDuration: `${duration}s`,
    animationDelay: `${Math.random() * 10}s`,
    opacity: Math.random() * 0.4 + 0.2
  };
};
</script>

<style scoped>
/* ====== 引入字体和图标库 ====== */
@import url('https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=Noto+Serif+SC:wght@300;400;600;700;900&family=Cinzel:wght@400;600;700&display=swap');
@import url("https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css");

/* ====== 核心配色系统 ====== */
:root {
  --bg-base: #f7f9f4;
  --ink-green: #1a3d2e;
  --sage-green: #2d5a47;
  --sage-green-light: #3d6b55;
  --light-green: #dcece6;
  --gold-accent: #c5a666;
  --gold-light: #d4b877;
  --paper-texture: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0IiBoZWlnaHQ9IjQiPgo8cmVjdCB3aWR0aD0iNCIgaGVpZ2h0PSI0IiBmaWxsPSIjZjdmOWY0Ii8+CjxyZWN0IHdpZHRoPSIxIiBoZWlnaHQ9IjEiIGZpbGw9IiNlMmU2ZTAiLz4KPC9zdmc+');
}

/* ====== 全局布局 ====== */
.herbal-archive {
  width: 100vw;
  min-height: 100vh;
  background-color: var(--bg-base);
  color: var(--ink-green);
  font-family: 'Noto Serif SC', serif;
  overflow-x: hidden;
  position: relative;
}

/* ====== 背景层系统 ====== */
.bg-layer {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.paper-texture {
  background-image: var(--paper-texture);
  opacity: 0.6;
}

.ink-blobs {
  z-index: 1;
  filter: blur(120px);
  opacity: 0.3;
}

.blob {
  position: absolute;
  border-radius: 50%;
  animation: breathe 15s infinite ease-in-out;
}

.blob-green-1 {
  width: 60vw;
  height: 60vw;
  background: var(--light-green);
  top: -20%;
  left: -15%;
  animation-duration: 18s;
}

.blob-gold-1 {
  width: 50vw;
  height: 50vw;
  background: rgba(197, 166, 102, 0.2);
  bottom: -10%;
  right: -10%;
  animation-duration: 20s;
  animation-delay: -5s;
}

.floating-particles {
  z-index: 2;
}

.particle {
  position: absolute;
  background: var(--gold-accent);
  border-radius: 50%;
  box-shadow: 0 0 8px rgba(197, 166, 102, 0.6);
  animation: floatUp linear infinite;
}

@keyframes breathe {
  from { transform: scale(1); }
  to { transform: scale(1.2); }
}

@keyframes floatUp {
  from {
    transform: translateY(100vh) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 0.8;
  }
  90% {
    opacity: 0.8;
  }
  to {
    transform: translateY(-10vh) rotate(360deg);
    opacity: 0;
  }
}

/* ====== 顶部控制区 ====== */
.archive-header {
  position: sticky;
  top: 0;
  padding: 25px 50px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(247, 249, 244, 0.85);
  backdrop-filter: blur(20px) saturate(180%);
  border-bottom: 1px solid rgba(44, 74, 62, 0.08);
  z-index: 100;
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.02);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 30px;
}

.back-btn {
  border: none;
  background: transparent;
  font-size: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--sage-green);
  padding: 10px 16px;
  border-radius: 10px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-family: 'Noto Serif SC', serif;
  font-weight: 500;
}

.back-btn:hover {
  color: var(--ink-green);
  background: rgba(45, 90, 71, 0.08);
  transform: translateX(-5px);
}

.back-btn i {
  font-size: 18px;
  transition: transform 0.3s ease;
}

.back-btn:hover i {
  transform: translateX(-3px);
}

.title-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.page-title {
  margin: 0;
  font-size: 32px;
  font-weight: 900;
  color: var(--ink-green);
  letter-spacing: 3px;
  display: flex;
  align-items: baseline;
  gap: 8px;
}

.title-main {
  font-family: 'Ma Shan Zheng', cursive;
  font-size: 36px;
}

.title-divider {
  color: var(--gold-accent);
  font-size: 24px;
  margin: 0 4px;
}

.title-sub {
  font-weight: 700;
  letter-spacing: 4px;
}

.title-desc {
  font-size: 11px;
  color: var(--sage-green);
  opacity: 0.7;
  letter-spacing: 2px;
  font-family: 'Cinzel', serif;
  margin: 0;
}

/* ====== 搜索框 ====== */
.search-bar {
  position: relative;
  width: 380px;
}

.search-bar input {
  width: 100%;
  padding: 14px 18px 14px 50px;
  border-radius: 30px;
  border: 2px solid rgba(45, 90, 71, 0.15);
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  outline: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-size: 15px;
  color: var(--ink-green);
  font-family: 'Noto Serif SC', serif;
}

.search-bar input::placeholder {
  color: rgba(45, 90, 71, 0.5);
}

.search-bar input:focus {
  border-color: var(--gold-accent);
  background: rgba(255, 255, 255, 1);
  box-shadow: 0 0 0 4px rgba(197, 166, 102, 0.15),
              0 8px 25px rgba(31, 59, 52, 0.1);
  transform: translateY(-2px);
}

.search-icon {
  position: absolute;
  left: 18px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--sage-green);
  font-size: 20px;
  pointer-events: none;
  transition: color 0.3s ease;
}

.search-bar input:focus + .search-glow {
  opacity: 1;
}

.search-glow {
  position: absolute;
  inset: -3px;
  border-radius: 30px;
  background: radial-gradient(circle, rgba(197, 166, 102, 0.2), transparent 70%);
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: -1;
}

.search-glow.active {
  opacity: 1;
}

/* ====== 过滤器 ====== */
.filter-bar {
  padding: 25px 50px;
  display: flex;
  align-items: center;
  gap: 25px;
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(44, 74, 62, 0.06);
  z-index: 90;
  position: relative;
}

.filter-label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--sage-green);
  font-weight: 600;
  font-size: 14px;
  white-space: nowrap;
}

.filter-label i {
  font-size: 18px;
}

.filter-tags {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.filter-tag {
  position: relative;
  padding: 10px 24px;
  border-radius: 25px;
  cursor: pointer;
  background: rgba(255, 255, 255, 0.8);
  color: var(--sage-green);
  font-size: 14px;
  font-weight: 500;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  border: 2px solid rgba(45, 90, 71, 0.1);
  overflow: hidden;
}

.filter-tag::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(197, 166, 102, 0.1), transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.filter-tag:hover {
  background: rgba(255, 255, 255, 1);
  border-color: var(--gold-accent);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(45, 90, 71, 0.12);
}

.filter-tag:hover::before {
  opacity: 1;
}

.filter-tag.active {
  background: linear-gradient(
    135deg,
    #3f7f64,
    #2d5a47
  );
  color: #ffffff;
  text-shadow: 0 1px 2px rgba(0,0,0,0.25);
  border-color: var(--gold-accent);
}


.filter-tag.active .tag-underline {
  width: 100%;
}

.tag-underline {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 2px;
  background: var(--gold-accent);
  transition: width 0.3s ease;
}

/* ====== 药材展示容器 ====== */
.herbs-container {
  flex: 1;
  padding: 40px 50px 60px;
  overflow-y: auto;
  position: relative;
  z-index: 10;
}

.herbs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 35px;
}

/* ====== 药材卡片 ====== */
.herb-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(12px);
  border-radius: 20px;
  padding: 30px;
  position: relative;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(255, 255, 255, 0.8);
  display: flex;
  flex-direction: column;
  box-shadow: 0 8px 25px rgba(31, 59, 52, 0.08),
              0 2px 10px rgba(0, 0, 0, 0.03);
}

.herb-card::before {
  content: '';
  position: absolute;
  inset: 0;
  padding: 2px;
  border-radius: 20px;
  pointer-events: none;
  }

.herb-card:hover {
  transform: translateY(-12px) scale(1.02);
  box-shadow: 0 20px 50px rgba(31, 59, 52, 0.15),
              0 8px 25px rgba(197, 166, 102, 0.2);
  border-color: var(--gold-accent);
}

.herb-card:hover::before {
  opacity: 1;
}

.card-bg-decoration {
  position: absolute;
  top: -50%;
  right: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(197, 166, 102, 0.05), transparent 70%);
  opacity: 0;
  transition: opacity 0.5s ease;
}

.herb-card:hover .card-bg-decoration {
  opacity: 1;
}

.card-bg-text {
  position: absolute;
  top: 20px;
  right: 20px;
  font-size: 72px;
  font-weight: 900;
  color: rgba(26, 61, 46, 0.04);
  font-family: 'Arial', sans-serif;
  pointer-events: none;
  letter-spacing: 2px;
  transition: transform 0.5s ease, opacity 0.5s ease;
}

.herb-card:hover .card-bg-text {
  transform: scale(1.1) translate(10px, -10px);
  opacity: 0.06;
}

/* 药材视觉区域 */
.herb-visual-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 25px;
  position: relative;
}

.herb-visual {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15),
              inset 0 0 20px rgba(255, 255, 255, 0.2);
  transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 2;
}

.herb-card:hover .herb-visual {
  transform: scale(1.15) rotate(5deg);
}

.herb-char {
  font-family: 'Ma Shan Zheng', cursive;
  font-size: 42px;
  color: #fff;
  text-shadow: 0 3px 10px rgba(0, 0, 0, 0.3);
  position: relative;
  z-index: 1;
}

.herb-glow {
  position: absolute;
  inset: -10px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.4), transparent 70%);
  opacity: 0;
  transition: opacity 0.5s ease;
  animation: pulse 3s ease-in-out infinite;
}

.herb-card:hover .herb-glow {
  opacity: 1;
}

.herb-category-badge {
  margin-top: 12px;
  padding: 4px 14px;
  background: rgba(45, 90, 71, 0.1);
  border: 1px solid rgba(45, 90, 71, 0.2);
  border-radius: 15px;
  font-size: 11px;
  color: var(--sage-green);
  font-weight: 600;
  letter-spacing: 1px;
  transition: all 0.3s ease;
}

.herb-card:hover .herb-category-badge {
  background: var(--gold-accent);
  color: #fff;
  border-color: var(--gold-accent);
  transform: scale(1.05);
}

/* 内容区域 */
.herb-content {
  flex: 1;
  margin-bottom: 20px;
}

.herb-name {
  font-size: 24px;
  font-weight: 700;
  margin: 0 0 6px;
  color: var(--ink-green);
  letter-spacing: 1px;
}

.herb-pinyin {
  font-size: 12px;
  color: var(--sage-green);
  opacity: 0.7;
  margin-bottom: 16px;
  font-family: 'Cinzel', serif;
  letter-spacing: 1px;
}

.herb-tags {
  display: flex;
  gap: 10px;
  margin-bottom: 16px;
}

.tag {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  padding: 6px 12px;
  border-radius: 20px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.tag.nature {
  background: linear-gradient(135deg, rgba(255, 152, 0, 0.15), rgba(255, 152, 0, 0.05));
  color: #e65100;
  border: 1px solid rgba(255, 152, 0, 0.3);
}

.tag.flavor {
  background: linear-gradient(135deg, rgba(156, 39, 176, 0.15), rgba(156, 39, 176, 0.05));
  color: #6a1b9a;
  border: 1px solid rgba(156, 39, 176, 0.3);
}

.tag i {
  font-size: 14px;
}

.herb-summary {
  font-size: 14px;
  color: #4a6659;
  line-height: 1.8;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin: 0;
}

/* 卡片底部 */
.card-footer {
  border-top: 1px dashed rgba(45, 90, 71, 0.15);
  padding-top: 18px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
}

.footer-text {
  font-size: 13px;
  color: var(--gold-accent);
  font-weight: 600;
  letter-spacing: 1px;
}

.footer-icon {
  font-size: 18px;
  color: var(--gold-accent);
  transition: transform 0.3s ease;
}

.herb-card:hover .footer-icon {
  transform: translateX(5px);
}

.footer-line {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--gold-accent);
  transition: width 0.5s ease;
}

.herb-card:hover .footer-line {
  width: 100%;
}

.card-hover-glow {
  position: absolute;
  inset: -2px;
  border-radius: 20px;
  background: radial-gradient(circle at center, rgba(197, 166, 102, 0.3), transparent 70%);
  opacity: 0.6;
  z-index: -1;
  animation: glowPulse 2s ease-in-out infinite;
}

@keyframes glowPulse {
  0%, 100% {
    opacity: 0.4;
  }
  50% {
    opacity: 0.8;
  }
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 0.6;
  }
  50% {
    transform: scale(1.1);
    opacity: 1;
  }
}

/* ====== 无结果提示 ====== */
.no-result {
  grid-column: 1 / -1;
  text-align: center;
  padding: 80px 20px;
}

.no-result-icon {
  font-size: 64px;
  color: var(--sage-green);
  opacity: 0.3;
  margin-bottom: 20px;
  animation: float 3s ease-in-out infinite;
}

.no-result h3 {
  font-size: 24px;
  color: var(--ink-green);
  margin: 0 0 10px;
}

.no-result p {
  font-size: 16px;
  color: var(--sage-green);
  opacity: 0.7;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

/* ====== 详情弹窗 ====== */
.detail-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.detail-book {
  width: 90%;
  max-width: 1000px;
  height: 85vh;
  max-height: 700px;
  background: #fff;
  border-radius: 20px;
  display: flex;
  overflow: hidden;
  box-shadow: 0 30px 80px rgba(0, 0, 0, 0.4),
              0 0 0 1px rgba(255, 255, 255, 0.1);
  position: relative;
  background-image:
    linear-gradient(to right, #fdfdfd 0%, #fff 48%, #f8f8f8 52%, #fafafa 100%);
}

.close-btn {
  position: absolute;
  top: 20px;
  right: 25px;
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  border-radius: 50%;
  font-size: 24px;
  cursor: pointer;
  color: #999;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  z-index: 10;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.close-btn:hover {
  background: var(--ink-green);
  color: #fff;
  transform: rotate(90deg) scale(1.1);
  box-shadow: 0 6px 20px rgba(31, 59, 52, 0.3);
}

/* 书页左侧 */
.book-left {
  flex: 0 0 42%;
  padding: 50px 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  background: linear-gradient(135deg, #fdfdfd 0%, #f9f9f9 100%);
}

.book-page-decoration {
  position: absolute;
  inset: 0;
  background-image:
    repeating-linear-gradient(
      90deg,
      transparent,
      transparent 48px,
      rgba(45, 90, 71, 0.03) 48px,
      rgba(45, 90, 71, 0.03) 50px
    );
  pointer-events: none;
}

.big-visual-wrapper {
  position: relative;
  margin-bottom: 50px;
  z-index: 2;
}

.big-visual {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Ma Shan Zheng', cursive;
  font-size: 72px;
  color: #fff;
  box-shadow:
    0 20px 60px rgba(0, 0, 0, 0.2),
    inset 0 0 30px rgba(255, 255, 255, 0.3);
  position: relative;
  margin: 0 auto;
  animation: visualFloat 4s ease-in-out infinite;
}

.big-char {
  position: relative;
  z-index: 2;
  text-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

.visual-rings {
  position: absolute;
  inset: -30px;
  border-radius: 50%;
  pointer-events: none;
}

.ring {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  border: 2px solid rgba(197, 166, 102, 0.3);
  animation: ringExpand 3s ease-in-out infinite;
}

.ring-2 {
  animation-delay: 1.5s;
  border-color: rgba(45, 90, 71, 0.2);
}

@keyframes visualFloat {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

@keyframes ringExpand {
  0% {
    transform: scale(1);
    opacity: 0.8;
  }
  100% {
    transform: scale(1.3);
    opacity: 0;
  }
}

.visual-label {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
  color: var(--sage-green);
  letter-spacing: 3px;
  font-weight: 600;
}

.meridians-section {
  width: 100%;
  text-align: center;
  margin-bottom: 30px;
}

.section-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 14px;
  color: var(--sage-green);
  margin-bottom: 18px;
  font-weight: 600;
  letter-spacing: 2px;
}

.section-title i {
  font-size: 18px;
  color: var(--gold-accent);
}

.meridian-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
}

.meridian-item {
  padding: 8px 20px;
  background: linear-gradient(135deg, rgba(197, 166, 102, 0.15), rgba(197, 166, 102, 0.05));
  border: 2px solid var(--gold-accent);
  border-radius: 25px;
  font-size: 15px;
  color: var(--ink-green);
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(197, 166, 102, 0.2);
  animation: fadeInUp 0.5s ease forwards;
  opacity: 0;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.category-display {
  margin-top: auto;
}

.category-tag-large {
  padding: 12px 34px;
  background: linear-gradient(
    135deg,
    #1a3d2e,
    #2d5a47
  );
  color: #fff;
  border-radius: 999px;
  font-size: 16px;
  font-weight: 800;
  letter-spacing: 3px;

  box-shadow:
    0 10px 28px rgba(31, 59, 52, 0.35),
    inset 0 1px 2px rgba(255,255,255,0.2);
}


/* 书页右侧 */
.book-right {
  flex: 1;
  padding: 50px 40px;
  overflow-y: auto;
  background: linear-gradient(135deg, #fff 0%, #fafafa 100%);
  position: relative;
}

.book-content {
  max-width: 100%;
}

.book-header {
  margin-bottom: 35px;
  padding-bottom: 25px;
  border-bottom: 2px solid rgba(197, 166, 102, 0.2);
}

.herb-title-main {
  font-size: 42px;
  margin: 0 0 8px;
  color: var(--ink-green);
  font-weight: 900;
  letter-spacing: 2px;
}

.herb-title-pinyin {
  font-size: 18px;
  color: var(--sage-green);
  opacity: 0.7;
  font-family: 'Cinzel', serif;
  letter-spacing: 3px;
  margin: 0;
}

.properties-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 35px;
}

.prop-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
  background: rgba(247, 249, 244, 0.8);
  border-radius: 15px;
  border: 1px solid rgba(45, 90, 71, 0.1);
  transition: all 0.3s ease;
}

.prop-item:hover {
  background: rgba(247, 249, 244, 1);
  border-color: var(--gold-accent);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(45, 90, 71, 0.1);
}

.prop-icon {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--gold-accent), var(--sage-green));
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 24px;
  box-shadow: 0 4px 12px rgba(197, 166, 102, 0.3);
}

.prop-content {
  flex: 1;
}

.prop-content label {
  display: block;
  font-size: 12px;
  color: var(--sage-green);
  opacity: 0.7;
  margin-bottom: 6px;
  letter-spacing: 1px;
}

.prop-content span {
  font-size: 18px;
  color: var(--ink-green);
  font-weight: 700;
}

.section {
  margin-bottom: 35px;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 18px;
}

.section-icon {
  font-size: 24px;
  color: var(--gold-accent);
}

.section-header h3 {
  font-size: 20px;
  color: var(--ink-green);
  margin: 0;
  font-weight: 700;
  letter-spacing: 1px;
}

.section-content {
  padding-left: 36px;
}

.section-content p {
  font-size: 16px;
  color: #4a6659;
  line-height: 2;
  text-align: justify;
  margin: 0;
}

/* 书页中缝 */
.book-spine {
  position: absolute;
  left: 50%;
  top: 0;
  bottom: 0;
  width: 2px;
  background: linear-gradient(
    to bottom,
    transparent,
    rgba(45, 90, 71, 0.1) 10%,
    rgba(45, 90, 71, 0.1) 90%,
    transparent
  );
  transform: translateX(-50%);
  box-shadow:
    -1px 0 3px rgba(0, 0, 0, 0.1),
    1px 0 3px rgba(0, 0, 0, 0.1);
}

/* ====== 动画 ====== */
.list-anim-enter-active {
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.list-anim-leave-active {
  transition: all 0.4s ease;
}

.list-anim-enter-from {
  opacity: 0;
  transform: translateY(30px) scale(0.9);
}

.list-anim-leave-to {
  opacity: 0;
  transform: scale(0.8);
}

.list-anim-move {
  transition: transform 0.5s ease;
}

.modal-pop-enter-active,
.modal-pop-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.modal-pop-enter-from,
.modal-pop-leave-to {
  opacity: 0;
}

.modal-pop-enter-from .detail-book,
.modal-pop-leave-to .detail-book {
  transform: scale(0.9) rotateY(10deg);
  opacity: 0;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* ====== 响应式设计 ====== */
@media (max-width: 1200px) {
  .herbs-grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 25px;
  }

  .detail-book {
    flex-direction: column;
    height: 90vh;
    max-height: none;
  }

  .book-left {
    flex: 0 0 auto;
    padding: 30px;
  }

  .book-spine {
    display: none;
  }
}

@media (max-width: 768px) {
  .archive-header {
    flex-direction: column;
    gap: 20px;
    padding: 20px;
  }

  .header-left {
    width: 100%;
    justify-content: space-between;
  }

  .search-bar {
    width: 100%;
  }

  .filter-bar {
    padding: 20px;
    flex-direction: column;
    align-items: flex-start;
  }

  .filter-tags {
    width: 100%;
  }

  .herbs-container {
    padding: 20px;
  }

  .herbs-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 20px;
  }

  .detail-overlay {
    padding: 20px;
  }

  .detail-book {
    width: 100%;
    height: 90vh;
  }

  .book-left,
  .book-right {
    padding: 25px;
  }

  .properties-grid {
    grid-template-columns: 1fr;
  }
}
</style>