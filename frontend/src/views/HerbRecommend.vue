<template>
  <div class="herb-recommend-page" v-cloak>
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
          <p>基于《全国中草药汇编》《中华本草》等权威资料</p>
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
          @click="handleCategoryChange(category.id)"
          :class="['category-btn', activeCategory === category.id ? 'active' : '']"
        >
          {{ category.name }} <span class="count">({{ getCategoryCount(category.id) }})</span>
        </button>
      </div>
    </div>

    <!-- 主要内容区 -->
    <div class="main-content">
      <!-- 加载中骨架屏 -->
      <div class="loading-skeleton" v-if="isLoading">
        <div class="skeleton-focus-card">
          <div class="skeleton-left">
            <div class="skeleton-badge"></div>
            <div class="skeleton-title"></div>
            <div class="skeleton-info"></div>
            <div class="skeleton-tags"></div>
            <div class="skeleton-text"></div>
            <div class="skeleton-text"></div>
            <div class="skeleton-btn"></div>
          </div>
          <div class="skeleton-right">
            <div class="skeleton-img"></div>
          </div>
        </div>
        <div class="skeleton-list-title"></div>
        <div class="skeleton-card-grid">
          <div class="skeleton-card" v-for="i in 6" :key="i"></div>
        </div>
      </div>

      <!-- 每日推荐焦点卡片 -->
      <div class="focus-card" v-else-if="Object.keys(focusHerb).length > 0">
        <div class="focus-left">
          <div class="badge">今日推荐</div>
          <h2>{{ focusHerb.name }}</h2>
          <div class="herb-basic-info">
            <span class="alias">别名：{{ focusHerb.alias }}</span>
            <span class="xingwei">性味：{{ focusHerb.xingwei }}</span>
            <span class="guijing" v-if="focusHerb.guijing !== '暂无数据'">归经：{{ focusHerb.guijing }}</span>
          </div>
          <div class="herb-tag">
            <span v-for="tag in focusHerb.tags" :key="tag">{{ tag }}</span>
          </div>
          <p class="desc">{{ focusHerb.brief }}</p>
          <div class="benefits">
            <h4>核心功效</h4>
            <ul>
              <li v-for="(benefit, idx) in focusHerb.benefits" :key="idx">{{ benefit }}</li>
            </ul>
          </div>
          <div class="usage-short">
            <h4>推荐用法</h4>
            <p>{{ focusHerb.usage }}</p>
          </div>
          <button class="detail-btn" @click="showHerbDetail(focusHerb)">查看完整详情</button>
        </div>
        <div class="focus-right">
          <div class="herb-img">
            <div class="img-placeholder" v-if="!imageLoaded"></div>
            <img
              :src="focusHerb.image"
              :alt="focusHerb.name"
              class="herb-photo"
              @error="handleImageError($event, focusHerb.name)"
              @load="imageLoaded = true"
              v-show="imageLoaded"
            />
          </div>
        </div>
      </div>

      <!-- 加载失败提示 -->
      <div class="loading-tip error" v-else>
        <p>❌ 中药数据加载失败</p>
        <p class="error-tip">请检查JSON文件路径是否正确：src/data/complete_herb_data.json</p>
      </div>

      <!-- 更多推荐列表 -->
      <div class="recommend-list" v-if="!isLoading && herbList.length > 0">
        <h3 class="list-title">更多中药推荐 <span>({{ filteredHerbs.length }})</span></h3>
        <div class="card-grid">
          <div
            v-for="herb in paginatedHerbs"
            :key="herb.id"
            class="herb-card"
            :style="{ height: '100%' }"
          >
            <div class="card-header">
              <div class="card-header-left">
                <div class="card-badge">{{ herb.category }}</div>
                <h4>{{ herb.name }}</h4>
                <p class="card-alias">{{ herb.alias }}</p>
              </div>
              <div class="card-header-right">
                <div class="card-img">
                  <div class="card-img-placeholder"></div>
                  <img
                    :src="`${herb.image}`"
                    :alt="herb.name"
                    class="card-photo"
                    @error="handleImageError($event, herb.name)"
                  />
                </div>
              </div>
            </div>
            <div class="card-body">
              <p class="card-brief">{{ herb.brief }}</p>
              <div class="card-tags">
                <span v-for="tag in herb.shortTags" :key="tag">{{ tag }}</span>
              </div>
              <div class="card-usage">
                <span>用法：{{ herb.usage }}</span>
              </div>
            </div>
            <div class="card-footer">
              <button class="card-btn" @click="showHerbDetail(herb)">了解更多</button>
            </div>
          </div>
        </div>

        <!-- 分页控件 -->
        <div class="pagination" v-if="totalPages > 1">
          <button
            class="page-btn"
            @click="changePage(currentPage - 1)"
            :disabled="currentPage === 1"
          >
            上一页
          </button>
          <span class="page-info">
            第 {{ currentPage }} 页 / 共 {{ totalPages }} 页
          </span>
          <button
            class="page-btn"
            @click="changePage(currentPage + 1)"
            :disabled="currentPage === totalPages"
          >
            下一页
          </button>
        </div>
      </div>
    </div>

    <!-- 药材详情弹窗 -->
    <teleport to="body">
      <div
        v-if="showDetailModal"
        class="detail-modal-overlay"
        @click="closeDetailModal"
        style="isolation: isolate; will-change: opacity;"
      >
        <div
          class="detail-modal"
          @click.stop
          style="isolation: isolate; will-change: transform; transform: translateZ(0);"
        >
          <div class="modal-header">
            <h3>{{ currentDetailHerb?.name }} 完整信息</h3>
            <button class="close-modal" @click="closeDetailModal">×</button>
          </div>
          <div class="modal-body">
            <div class="modal-left">
              <div class="modal-img-placeholder" v-if="!modalImageLoaded"></div>
              <img
                :src="currentDetailHerb?.image"
                :alt="currentDetailHerb?.name"
                class="modal-photo"
                @error="handleImageError($event, currentDetailHerb?.name)"
                @load="modalImageLoaded = true"
                v-show="modalImageLoaded"
              />
              <div class="modal-category">{{ currentDetailHerb?.category }}</div>
              <div class="modal-basic">
                <p><strong>药材ID：</strong>{{ currentDetailHerb?.herbId }}</p>
                <p><strong>别名：</strong>{{ currentDetailHerb?.alias }}</p>
                <p><strong>性味：</strong>{{ currentDetailHerb?.xingwei }}</p>
                <p><strong>归经：</strong>{{ currentDetailHerb?.guijing || '暂无数据' }}</p>
              </div>
            </div>
            <div class="modal-right">
              <div class="modal-section">
                <h4>功能主治</h4>
                <p class="modal-content">{{ currentDetailHerb?.brief || '暂无数据' }}</p>
              </div>
              <div class="modal-section">
                <h4>核心功效</h4>
                <ul class="modal-list">
                  <li v-for="(benefit, idx) in currentDetailHerb?.benefits" :key="idx">{{ benefit }}</li>
                </ul>
              </div>
              <div class="modal-section">
                <h4>用法用量</h4>
                <p class="modal-content">{{ currentDetailHerb?.usage }}</p>
              </div>
              <div class="modal-section" v-if="currentDetailHerb?.warning !== '暂无数据'">
                <h4>注意事项</h4>
                <p class="modal-content">{{ currentDetailHerb?.warning }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </teleport>

    <!-- 底部信息 -->
    <div class="page-footer">
      <p>© 2025 中药智能推荐平台 | 数据来源：《全国中草药汇编》《中华本草》《中药大辞典》等</p>
      <p class="disclaimer">免责声明：本平台信息仅供参考，使用前请咨询专业中医师</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";

// ===================== 1. 状态初始化 =====================
const currentDate = ref("");
const categories = ref([]);
const activeCategory = ref('all');
const showDetailModal = ref(false);
const currentDetailHerb = ref(null);
const focusHerb = ref({});
const herbList = ref([]);
const isLoading = ref(true);
const imageLoaded = ref(false);
const modalImageLoaded = ref(false);
const currentPage = ref(1);
const pageSize = ref(20);

// ===================== 2. 异步加载JSON数据（恢复真实JSON加载） =====================
onMounted(async () => {
  try {
    // 方案2：加载真实JSON数据（替换模拟数据）
    const response = await import('@/data/complete_herb_data.json');
    const data = response.default;

    // 延迟赋值，模拟加载效果
    setTimeout(() => {
      focusHerb.value = data.focusHerb;
      herbList.value = data.herbList;
      categories.value = data.categories;
      isLoading.value = false;
      initDate();
      console.log(`✅ 真实JSON数据加载成功，共加载 ${data.totalCount} 条药材数据`);
    }, 100);

    // 方案1：模拟数据（已注释，如需测试可取消注释）
    // const mockData = { ... };
    // setTimeout(() => { ... }, 100);

  } catch (error) {
    console.error("❌ 加载真实JSON数据失败：", error);
    console.error("排查方向：");
    console.error("1. 检查文件路径：src/data/complete_herb_data.json 是否存在");
    console.error("2. 检查JSON格式：是否有语法错误（如逗号多余、引号不匹配）");
    console.error("3. 检查import路径：@/data/ 对应 src/data/ 目录");
    isLoading.value = false;
  }
});
// ===================== 3. 计算属性 =====================
const filteredHerbs = computed(() => {
  if (activeCategory.value === 'all') {
    return herbList.value;
  }
  return herbList.value.filter(herb => herb.categoryId === activeCategory.value);
});

const paginatedHerbs = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  return filteredHerbs.value.slice(start, end);
});

const totalPages = computed(() => {
  return Math.ceil(filteredHerbs.value.length / pageSize.value);
});

// ===================== 4. 方法定义 =====================
const goToHome = () => {
  window.location.href = '/';
};

// 核心：显示详情弹窗
const showHerbDetail = (herb) => {
  currentDetailHerb.value = herb;
  showDetailModal.value = true;
  modalImageLoaded.value = false;
};

// 关闭详情弹窗
const closeDetailModal = () => {
  showDetailModal.value = false;
  setTimeout(() => {
    currentDetailHerb.value = null;
  }, 100);
};

// 图片加载失败处理
const handleImageError = (e, herbName) => {
  console.warn(`【${herbName}】图片加载失败，使用默认图片`, e.target.src);
  e.target.src = '/pictures/default_herb.jpg';
  e.target.onerror = function() {
    this.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNzAiIGhlaWdodD0iNzAiIHZpZXdCb3g9IjAgMCA3MCA3MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMzUiIGN5PSIzNSIgcj0iMzUiIGZpbGw9IiNmMGY4ZjAiLz4KPHBhdGggZD0iTTI1IDM1QzI1IDQxLjA3NSAyOS45MjUgNDYgMzUgNDZDQzQwLjA3NSA0NiA0NSA0MS4wNzUgNDUgMzVDNDUgMjguOTI1IDQwLjA3NSAyNCAzNSAyNEMyOS45MjUgMjQgMjUgMjguOTI1IDI1IDM1WiIgZmlsbD0iIzQzNzg2YSIvPgo8cGF0aCBkPSJNMzUgMjVWNDUiIGZpbGw9IiM0Mzc4NmEiIHN0cm9rZT0iIzQzNzg2YSIgc3Ryb2tlLXdpZHRoPSIyIi8+CjxwYXRoIGQ9Ik0yNSA0NUw0NSAzNSIgc3Ryb2tlPSIjNDM3ODZhIiBzdHJva2Utd2lkdGg9IjIiLz4KPC9zdmc+';
    this.alt = herbName + '（默认图片）';
  };
};

// 获取分类药材数量
const getCategoryCount = (categoryId) => {
  if (categoryId === 'all') return herbList.value.length;
  return herbList.value.filter(herb => herb.categoryId === categoryId).length;
};

// 分类切换
const handleCategoryChange = (categoryId) => {
  currentPage.value = 1;
  setTimeout(() => {
    activeCategory.value = categoryId;
    const listElement = document.querySelector('.recommend-list');
    if (listElement) {
      listElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }, 50);
};

// 分页切换
const changePage = (page) => {
  if (page < 1 || page > totalPages.value) return;
  currentPage.value = page;
  const listElement = document.querySelector('.recommend-list');
  if (listElement) {
    listElement.scrollIntoView({ behavior: 'smooth' });
  }
};

// 初始化日期
const initDate = () => {
  const date = new Date();
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const week = ['日', '一', '二', '三', '四', '五', '六'][date.getDay()];
  currentDate.value = `${year}年${month}月${day}日 星期${week}`;
};
</script>

<style scoped>
/* 保留你原有所有样式代码 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: "Inter", "PingFang SC", "Microsoft YaHei", sans-serif;
}

[v-cloak] {
  display: none !important;
}

.herb-recommend-page {
  width: 100vw;
  min-height: 100vh;
  background: linear-gradient(180deg, #f0f8f0 0%, #e6f5e6 100%);
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
  overflow-anchor: none;
}

.loading-skeleton {
  padding: 24px 0;
}

.skeleton-focus-card {
  display: flex;
  gap: 24px;
  background: white;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 32px;
}

.skeleton-left {
  flex: 3;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.skeleton-badge {
  width: 80px;
  height: 24px;
  background: #f0f8f0;
  border-radius: 12px;
  animation: skeleton-loading 1.5s infinite;
}

.skeleton-title {
  width: 200px;
  height: 32px;
  background: #f0f8f0;
  border-radius: 8px;
  animation: skeleton-loading 1.5s infinite;
}

.skeleton-info {
  width: 300px;
  height: 20px;
  background: #f0f8f0;
  border-radius: 8px;
  animation: skeleton-loading 1.5s infinite;
}

.skeleton-tags {
  width: 250px;
  height: 24px;
  background: #f0f8f0;
  border-radius: 12px;
  animation: skeleton-loading 1.5s infinite;
}

.skeleton-text {
  width: 100%;
  height: 80px;
  background: #f0f8f0;
  border-radius: 8px;
  animation: skeleton-loading 1.5s infinite;
}

.skeleton-btn {
  width: 120px;
  height: 36px;
  background: #f0f8f0;
  border-radius: 8px;
  animation: skeleton-loading 1.5s infinite;
}

.skeleton-right {
  flex: 1;
  display: flex;
  justify-content: center;
}

.skeleton-img {
  width: 220px;
  height: 220px;
  background: #f0f8f0;
  border-radius: 12px;
  animation: skeleton-loading 1.5s infinite;
}

.skeleton-list-title {
  width: 200px;
  height: 28px;
  background: #f0f8f0;
  border-radius: 8px;
  margin-bottom: 20px;
  animation: skeleton-loading 1.5s infinite;
}

.skeleton-card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
}

.skeleton-card {
  height: 380px;
  background: #f0f8f0;
  border-radius: 12px;
  animation: skeleton-loading 1.5s infinite;
}

@keyframes skeleton-loading {
  0% { background-color: #f0f8f0; }
  50% { background-color: #e8f5e9; }
  100% { background-color: #f0f8f0; }
}

.loading-tip {
  text-align: center;
  padding: 40px 0;
  color: #6b8c82;
  font-size: 16px;
}

.loading-tip.error {
  color: #e53e3e;
}

.error-tip {
  font-size: 12px;
  margin-top: 8px;
  color: #94a3b8;
}

.page-header {
  background: linear-gradient(90deg, #43786a 0%, #2d5d50 100%);
  padding: 16px 24px;
  color: white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  will-change: background;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1400px;
  margin: 0 auto;
}

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
  will-change: background;
}

.back-home-btn:hover {
  background-color: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.4);
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.page-title {
  text-align: center;
}

.page-title h1 {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 4px;
}

.page-title p {
  font-size: 12px;
  opacity: 0.8;
}

.date-display {
  font-size: 14px;
  opacity: 0.9;
  white-space: nowrap;
}

.category-nav {
  background: white;
  padding: 12px 0;
  border-bottom: 1px solid #e8f0e8;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  will-change: transform;
}

.nav-wrapper {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  overflow-x: auto;
  gap: 12px;
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
  display: flex;
  align-items: center;
  gap: 6px;
  flex-shrink: 0;
}

.category-btn .count {
  font-size: 12px;
  color: #6b8c82;
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

.category-btn.active .count {
  color: white;
  opacity: 0.9;
}

.main-content {
  flex: 1;
  max-width: 1400px;
  margin: 0 auto;
  padding: 24px;
}

.focus-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(67, 120, 106, 0.12);
  padding: 24px;
  margin-bottom: 32px;
  display: flex;
  gap: 24px;
  align-items: flex-start;
  will-change: box-shadow;
}

.focus-left {
  flex: 3;
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
  margin-bottom: 8px;
}

.herb-basic-info {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 16px;
  font-size: 14px;
  color: #6b8c82;
}

.herb-tag {
  display: flex;
  flex-wrap: wrap;
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
  line-height: 1.8;
  margin-bottom: 20px;
  font-size: 15px;
}

.benefits, .usage-short {
  margin-bottom: 20px;
}

.benefits h4, .usage-short h4 {
  color: #2d5d50;
  font-size: 16px;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.benefits ul {
  list-style: none;
  padding-left: 24px;
}

.benefits li {
  padding-left: 8px;
  position: relative;
  color: #4a5568;
  line-height: 1.8;
  font-size: 14px;
}

.benefits li::before {
  content: "•";
  position: absolute;
  left: -16px;
  color: #43786a;
  font-weight: bold;
}

.usage-short p {
  color: #4a5568;
  line-height: 1.6;
  font-size: 14px;
  padding-left: 24px;
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
  will-change: transform;
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
  width: 220px;
  height: 220px;
  border-radius: 12px;
  overflow: hidden;
  border: 4px solid #f0f8f0;
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
  position: relative;
}

.img-placeholder {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: #f0f8f0;
  animation: skeleton-loading 1.5s infinite;
}

.herb-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

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
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
  grid-auto-rows: 1fr;
}

.herb-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(67, 120, 106, 0.08);
  overflow: hidden;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  will-change: transform, box-shadow;
}

.herb-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(67, 120, 106, 0.12);
}

.card-header {
  padding: 16px;
  border-bottom: 1px solid #e8f0e8;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-shrink: 0;
}

.card-header-left {
  flex: 1;
  margin-right: 12px;
}

.card-header-right {
  flex: 0 0 70px;
}

.card-img {
  width: 70px;
  height: 70px;
  border-radius: 8px;
  overflow: hidden;
  border: 2px solid #f0f8f0;
  position: relative;
}

.card-img-placeholder {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: #f0f8f0;
  z-index: 1;
}

.card-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
  position: relative;
  z-index: 2;
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
  margin-bottom: 4px;
}

.card-alias {
  font-size: 12px;
  color: #6b8c82;
}

.card-body {
  padding: 16px;
  flex: 1;
  flex-shrink: 0;
}

.card-brief {
  color: #4a5568;
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 12px;
}

.card-tags span {
  padding: 2px 8px;
  background: #f0f8f0;
  border-radius: 4px;
  font-size: 12px;
  color: #6b8c82;
}

.card-usage {
  font-size: 12px;
  color: #43786a;
  line-height: 1.4;
}

.card-footer {
  padding: 12px 16px;
  border-top: 1px solid #e8f0e8;
  background: #f8fcf8;
  flex-shrink: 0;
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
  will-change: background, color;
}

.card-btn:hover {
  background: #43786a;
  color: white;
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-top: 32px;
  padding: 16px;
}

.page-btn {
  padding: 8px 16px;
  background: #f8fcf8;
  border: 1px solid #e8f0e8;
  border-radius: 6px;
  color: #43786a;
  cursor: pointer;
  transition: all 0.2s ease;
}

.page-btn:hover:not(:disabled) {
  background: #e8f5e9;
  border-color: #d0e6d0;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  font-size: 14px;
  color: #6b8c82;
}

.detail-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 20px;
  backdrop-filter: blur(2px);
}

.detail-modal {
  background: white;
  border-radius: 16px;
  width: 100%;
  max-width: 1000px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 8px 40px rgba(0,0,0,0.2);
  transform: translateZ(0);
  backface-visibility: hidden;
}

.modal-img-placeholder {
  width: 240px;
  height: 240px;
  border-radius: 12px;
  background: #f0f8f0;
  animation: skeleton-loading 1.5s infinite;
  margin-bottom: 16px;
  border: 3px solid #f0f8f0;
}

.modal-header {
  padding: 20px;
  border-bottom: 1px solid #e8f0e8;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  background: white;
  z-index: 10;
}

.modal-header h3 {
  color: #2d5d50;
  font-size: 20px;
}

.close-modal {
  background: transparent;
  border: none;
  font-size: 24px;
  color: #999;
  cursor: pointer;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.close-modal:hover {
  background: #f0f8f0;
  color: #2d5d50;
}

.modal-body {
  padding: 24px;
  display: flex;
  gap: 24px;
}

.modal-left {
  flex: 0 0 240px;
}

.modal-photo {
  width: 240px;
  height: 240px;
  border-radius: 12px;
  object-fit: cover;
  border: 3px solid #f0f8f0;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  margin-bottom: 16px;
}

.modal-category {
  padding: 4px 12px;
  background: #e8f5e9;
  color: #43786a;
  border-radius: 20px;
  font-size: 12px;
  text-align: center;
  margin-bottom: 16px;
}

.modal-basic {
  background: #f8fcf8;
  border-radius: 8px;
  padding: 12px;
}

.modal-basic p {
  font-size: 14px;
  color: #4a5568;
  line-height: 1.8;
}

.modal-basic strong {
  color: #2d5d50;
}

.modal-right {
  flex: 1;
}

.modal-section {
  margin-bottom: 20px;
}

.modal-section h4 {
  color: #2d5d50;
  font-size: 16px;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.modal-content {
  color: #4a5568;
  line-height: 1.8;
  font-size: 14px;
  text-align: justify;
}

.modal-list {
  list-style: none;
  padding-left: 24px;
}

.modal-list li {
  padding-left: 8px;
  position: relative;
  color: #4a5568;
  line-height: 1.8;
  font-size: 14px;
}

.modal-list li::before {
  content: "•";
  position: absolute;
  left: -16px;
  color: #43786a;
  font-weight: bold;
}

.page-footer {
  padding: 20px 24px;
  text-align: center;
  font-size: 12px;
  color: #6b8c82;
  background: transparent;
  border-top: 1px solid #e8f0e8;
  margin-top: 40px;
}

.page-footer .disclaimer {
  margin-top: 8px;
  font-size: 11px;
  color: #94a3b8;
}

@media (max-width: 992px) {
  .focus-card {
    flex-direction: column;
  }

  .focus-left, .focus-right {
    width: 100%;
  }

  .herb-img {
    width: 100%;
    max-width: 240px;
    margin: 0 auto 16px;
  }

  .modal-body {
    flex-direction: column;
  }

  .modal-left {
    flex: 0 0 auto;
    text-align: center;
    margin: 0 auto;
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .card-grid {
    grid-template-columns: 1fr;
  }

  .main-content {
    padding: 16px;
  }

  .focus-left h2 {
    font-size: 24px;
  }
}
</style>