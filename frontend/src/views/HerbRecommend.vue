<template>
  <div class="herb-recommend-page">
    <!-- 顶部导航栏（含返回首页按钮） -->
    <div class="page-header">
      <div class="header-content">
        <!-- 返回首页按钮 -->
        <button @click="goToHome" class="back-home-btn">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M19 12H5M5 12L12 19M5 12L12 5" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>返回首页</span>
        </button>

        <!-- 页面标题 -->
        <div class="page-title">
          <h1>🌿 中药智能推荐</h1>
          <p>每日精选 · 对症调理</p>
        </div>

        <!-- 日期显示 -->
        <div class="date-display">
          {{ currentDate }}
        </div>
      </div>
    </div>

    <!-- 分类导航 -->
    <div class="category-nav">
      <div class="nav-wrapper">
        <button
          v-for="category in categories"
          :key="category.id"
          @click="activeCategory = category.id"
          :class="['category-btn', activeCategory === category.id ? 'active' : '']"
        >
          {{ category.name }}
        </button>
      </div>
    </div>

    <!-- 主要内容区 -->
    <div class="main-content">
      <!-- 每日推荐焦点卡片 -->
      <div class="focus-card">
        <div class="focus-left">
          <div class="badge">今日推荐</div>
          <h2>{{ focusHerb.name }}</h2>
          <div class="herb-tag">
            <span v-for="tag in focusHerb.tags" :key="tag">{{ tag }}</span>
          </div>
          <p class="desc">{{ focusHerb.desc }}</p>
          <div class="benefits">
            <h4>核心功效</h4>
            <ul>
              <li v-for="benefit in focusHerb.benefits" :key="benefit">{{ benefit }}</li>
            </ul>
          </div>
          <button class="detail-btn">查看详情</button>
        </div>
        <div class="focus-right">
          <div class="herb-img">
            <svg width="200" height="200" viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="100" cy="100" r="90" fill="#f0f8f0" stroke="#43786a" stroke-width="2"/>
              <path d="M60 80C60 65 75 55 90 60C105 65 110 80 110 95C110 110 100 120 90 125C80 130 70 135 60 125C50 115 50 100 60 80Z" fill="#43786a"/>
              <path d="M100 70C100 55 115 45 130 50C145 55 150 70 150 85C150 100 140 110 130 115C120 120 110 125 100 115C90 105 90 90 100 70Z" fill="#2d5d50"/>
              <path d="M80 110C80 95 95 85 110 90C125 95 130 110 130 125C130 140 120 150 110 155C100 160 90 165 80 155C70 145 70 130 80 110Z" fill="#6b8c82"/>
            </svg>
          </div>
          <div class="usage-tip">
            <p>💡 推荐用法：{{ focusHerb.usage }}</p>
          </div>
        </div>
      </div>

      <!-- 更多推荐列表 -->
      <div class="recommend-list">
        <h3 class="list-title">更多推荐 <span>({{ filteredHerbs.length }})</span></h3>
        <div class="card-grid">
          <div
            v-for="herb in filteredHerbs"
            :key="herb.id"
            class="herb-card"
          >
            <div class="card-header">
              <div class="card-badge">{{ herb.category }}</div>
              <h4>{{ herb.name }}</h4>
            </div>
            <div class="card-body">
              <p>{{ herb.brief }}</p>
              <div class="card-tags">
                <span v-for="tag in herb.shortTags" :key="tag">{{ tag }}</span>
              </div>
            </div>
            <div class="card-footer">
              <button class="card-btn">了解更多</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 底部信息 -->
    <div class="page-footer">
      <p>© 2026  老中医智能AI推荐平台 | 本推荐仅供参考，使用前请咨询专业中医师</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
// 如果使用Vue Router，取消下面注释
// import { useRouter } from "vue-router";
// const router = useRouter();

// 返回首页函数
const goToHome = () => {
  // 方式1：Vue Router跳转
  // router.push('/');

  // 方式2：原生跳转
  window.location.href = '/';

  // 方式3：测试提示
  // alert('返回首页');
};

// 当前日期
const currentDate = ref("");
// 分类数据
const categories = ref([
  { id: 'all', name: '全部' },
  { id: 'qi', name: '补气' },
  { id: 'xue', name: '补血' },
  { id: 'yin', name: '滋阴' },
  { id: 'yang', name: '补阳' },
  { id: 'qingre', name: '清热' },
  { id: 'qushi', name: '祛湿' }
]);
// 激活的分类
const activeCategory = ref('all');

// 今日焦点推荐药材
const focusHerb = ref({
  name: '黄芪',
  tags: ['补气', '健脾', '益卫固表'],
  desc: '黄芪为豆科植物蒙古黄芪的干燥根，是传统的补气良药。性温，味甘，归脾、肺经。每日适量食用，可有效改善气虚乏力、食少便溏等症状，尤其适合现代上班族调理身体。',
  benefits: [
    '补气升阳，用于气虚乏力，中气下陷',
    '固表止汗，用于气虚自汗，阴虚盗汗',
    '利水消肿，用于气虚水肿，小便不利',
    '生津养血，用于气虚血亏，内热消渴'
  ],
  usage: '黄芪10-15g，泡水代茶饮，或与红枣、枸杞同煮'
});

// 推荐药材列表
const herbList = ref([
  {
    id: 1,
    name: '当归',
    category: '补血',
    brief: '补血活血，调经止痛，润肠通便。适用于血虚萎黄，眩晕心悸。',
    shortTags: ['补血', '调经', '活血'],
    categoryId: 'xue'
  },
  {
    id: 2,
    name: '枸杞',
    category: '滋阴',
    brief: '滋补肝肾，益精明目。适用于肝肾阴虚，头晕目眩，视力减退。',
    shortTags: ['滋阴', '明目', '养肝'],
    categoryId: 'yin'
  },
  {
    id: 3,
    name: '人参',
    category: '补气',
    brief: '大补元气，复脉固脱，益气健脾。适用于体虚欲脱，肢冷脉微。',
    shortTags: ['补气', '安神', '健脾'],
    categoryId: 'qi'
  },
  {
    id: 4,
    name: '鹿茸',
    category: '补阳',
    brief: '壮肾阳，益精血，强筋骨。适用于肾阳不足，精血亏虚，阳痿滑精。',
    shortTags: ['补阳', '益精', '强骨'],
    categoryId: 'yang'
  },
  {
    id: 5,
    name: '金银花',
    category: '清热',
    brief: '清热解毒，疏散风热。适用于痈肿疔疮，喉痹，丹毒，风热感冒。',
    shortTags: ['清热', '解毒', '解表'],
    categoryId: 'qingre'
  },
  {
    id: 6,
    name: '薏米',
    category: '祛湿',
    brief: '利水渗湿，健脾止泻，清热排脓。适用于水肿，脚气，小便不利。',
    shortTags: ['祛湿', '健脾', '消肿'],
    categoryId: 'qushi'
  },
  {
    id: 7,
    name: '麦冬',
    category: '滋阴',
    brief: '养阴生津，润肺清心。适用于肺燥干咳，阴虚痨嗽，津伤口渴。',
    shortTags: ['滋阴', '润肺', '生津'],
    categoryId: 'yin'
  },
  {
    id: 8,
    name: '肉桂',
    category: '补阳',
    brief: '补火助阳，引火归元，散寒止痛。适用于阳痿宫冷，腰膝冷痛。',
    shortTags: ['补阳', '散寒', '止痛'],
    categoryId: 'yang'
  }
]);

// 根据分类筛选药材
const filteredHerbs = computed(() => {
  if (activeCategory.value === 'all') {
    return herbList.value;
  }
  return herbList.value.filter(herb => herb.categoryId === activeCategory.value);
});

// 初始化日期
const initDate = () => {
  const date = new Date();
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const week = ['日', '一', '二', '三', '四', '五', '六'][date.getDay()];
  currentDate.value = `${year}年${month}月${day}日 星期${week}`;
};

// 页面挂载时初始化
onMounted(() => {
  initDate();
});
</script>

<style scoped>
/* 全局样式重置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: "Inter", "PingFang SC", "Microsoft YaHei", sans-serif;
}

.herb-recommend-page {
  width: 100vw;
  min-height: 100vh;
  background: linear-gradient(180deg, #f0f8f0 0%, #e6f5e6 100%);
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
}

/* 顶部导航栏 */
.page-header {
  background: linear-gradient(90deg, #43786a 0%, #2d5d50 100%);
  padding: 16px 24px;
  color: white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
}

/* 返回首页按钮 */
.back-home-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background-color: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  color: white;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.back-home-btn:hover {
  background-color: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.4);
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.back-home-btn:active {
  transform: scale(0.98);
}

/* 页面标题 */
.page-title {
  text-align: center;
}

.page-title h1 {
  font-size: 22px;
  font-weight: 600;
  margin-bottom: 4px;
}

.page-title p {
  font-size: 12px;
  opacity: 0.8;
}

/* 日期显示 */
.date-display {
  font-size: 14px;
  opacity: 0.9;
  white-space: nowrap;
}

/* 分类导航 */
.category-nav {
  background: white;
  padding: 12px 0;
  border-bottom: 1px solid #e8f0e8;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.nav-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  overflow-x: auto;
  gap: 8px;
  padding: 0 24px;
  scrollbar-width: none;
}

.nav-wrapper::-webkit-scrollbar {
  display: none;
}

.category-btn {
  padding: 8px 16px;
  background: #f8fcf8;
  border: 1px solid #e8f0e8;
  border-radius: 20px;
  color: #43786a;
  font-size: 14px;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s ease;
}

.category-btn:hover {
  background: #e8f5e9;
  border-color: #d0e6d0;
}

.category-btn.active {
  background: linear-gradient(90deg, #43786a 0%, #2d5d50 100%);
  color: white;
  border-color: #43786a;
}

/* 主要内容区 */
.main-content {
  flex: 1;
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
}

/* 焦点卡片 */
.focus-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(67, 120, 106, 0.12);
  padding: 24px;
  margin-bottom: 32px;
  display: flex;
  gap: 24px;
  align-items: center;
}

.focus-left {
  flex: 2;
}

.badge {
  display: inline-block;
  padding: 4px 12px;
  background: linear-gradient(90deg, #43786a 0%, #2d5d50 100%);
  color: white;
  border-radius: 20px;
  font-size: 12px;
  margin-bottom: 12px;
}

.focus-left h2 {
  font-size: 28px;
  color: #2d5d50;
  margin-bottom: 12px;
}

.herb-tag {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

.herb-tag span {
  padding: 4px 12px;
  background: #f0f8f0;
  border: 1px solid #e8f0e8;
  border-radius: 16px;
  font-size: 12px;
  color: #43786a;
}

.focus-left .desc {
  color: #4a5568;
  line-height: 1.6;
  margin-bottom: 20px;
  font-size: 15px;
}

.benefits h4 {
  color: #2d5d50;
  font-size: 16px;
  margin-bottom: 8px;
}

.benefits ul {
  list-style: none;
  margin-bottom: 24px;
}

.benefits li {
  padding-left: 20px;
  position: relative;
  color: #4a5568;
  line-height: 1.8;
  font-size: 14px;
}

.benefits li::before {
  content: "✓";
  position: absolute;
  left: 0;
  color: #43786a;
  font-weight: bold;
}

.detail-btn {
  padding: 10px 24px;
  background: linear-gradient(90deg, #43786a 0%, #2d5d50 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.detail-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(67, 120, 106, 0.2);
}

.focus-right {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.herb-img {
  margin-bottom: 16px;
}

.usage-tip {
  background: #f8fcf8;
  border-radius: 12px;
  padding: 12px 16px;
  width: 100%;
}

.usage-tip p {
  color: #43786a;
  font-size: 14px;
  line-height: 1.5;
}

/* 推荐列表 */
.recommend-list {
  margin-top: 32px;
}

.list-title {
  color: #2d5d50;
  font-size: 20px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.list-title span {
  font-size: 14px;
  color: #6b8c82;
  font-weight: normal;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.herb-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(67, 120, 106, 0.08);
  overflow: hidden;
  transition: all 0.3s ease;
}

.herb-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(67, 120, 106, 0.12);
}

.card-header {
  padding: 16px;
  border-bottom: 1px solid #e8f0e8;
}

.card-badge {
  display: inline-block;
  padding: 2px 8px;
  background: #e8f5e9;
  color: #43786a;
  border-radius: 4px;
  font-size: 12px;
  margin-bottom: 8px;
}

.card-header h4 {
  color: #2d5d50;
  font-size: 18px;
}

.card-body {
  padding: 16px;
}

.card-body p {
  color: #4a5568;
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 12px;
}

.card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.card-tags span {
  padding: 2px 8px;
  background: #f0f8f0;
  border-radius: 4px;
  font-size: 12px;
  color: #6b8c82;
}

.card-footer {
  padding: 12px 16px;
  border-top: 1px solid #e8f0e8;
  background: #f8fcf8;
}

.card-btn {
  width: 100%;
  padding: 8px 0;
  background: transparent;
  border: 1px solid #43786a;
  color: #43786a;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.card-btn:hover {
  background: #43786a;
  color: white;
}

/* 底部信息 */
.page-footer {
  padding: 16px 24px;
  text-align: center;
  font-size: 12px;
  color: #6b8c82;
  background: transparent;
  border-top: 1px solid #e8f0e8;
  margin-top: 40px;
}


</style>