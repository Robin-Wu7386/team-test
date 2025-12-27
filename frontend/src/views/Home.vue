<template>
  <div class="tcm-home" @mousemove="handleMouseMove" @scroll="handleScroll">
    <!-- ================= 1. 多层次背景系统 ================= -->
    <!-- 宣纸纹理底色 -->
    <div class="bg-layer paper-texture"></div>

    <!-- 水墨晕染层 (多层叠加) -->
    <div class="bg-layer ink-blobs">
      <div class="blob blob-green-1"></div>
      <div class="blob blob-green-2"></div>
      <div class="blob blob-gold-1"></div>
      <div class="blob blob-gold-2"></div>
      <div class="blob blob-amber"></div>
    </div>

    <!-- 背景装饰纹理 - 本草图案 -->
    <div class="bg-layer herb-pattern-layer">
      <div class="herb-pattern herb-pattern-1"></div>
      <div class="herb-pattern herb-pattern-2"></div>
      <div class="herb-pattern herb-pattern-3"></div>
    </div>

    <!-- 全局悬浮粒子 -->
    <div class="bg-layer particles">
      <div v-for="n in 50" :key="n" class="particle" :style="getParticleStyle(n)"></div>
    </div>

    <!-- 能量波纹效果 -->
    <div class="bg-layer energy-waves">
      <div class="wave wave-1"></div>
      <div class="wave wave-2"></div>
      <div class="wave wave-3"></div>
    </div>

    <!-- ================= 2. 顶部导航栏 ================= -->
    <header class="glass-nav" :class="{ scrolled: isScrolled }">
      <!-- 左侧：Logo + 本草植物群 -->
      <div class="nav-left">
        <div class="logo-area">
          <!-- 本草植物群容器 -->
          <div class="herb-garden">
            <!-- 主要本草植物 - 中心株 -->
            <svg class="main-herb" viewBox="0 0 120 140" xmlns="http://www.w3.org/2000/svg">
              <!-- 主茎 -->
              <path d="M60 130 L60 100 Q58 85 60 70 Q62 55 60 40 Q58 30 60 20 Q62 12 60 8 Q58 5 60 2"
                    stroke="#1a3d2e" stroke-width="4" fill="none"
                    stroke-linecap="round" stroke-linejoin="round" class="herb-stem-main"/>

              <!-- 左侧大叶子组 -->
              <g class="leaf-group-left">
                <path d="M60 95 Q45 88 38 95 Q42 102 55 98 Q60 96 60 95"
                      stroke="#2d5a47" stroke-width="3" fill="#3d6b55"
                      opacity="0.85" class="leaf leaf-large leaf-1"/>
                <path d="M60 75 Q50 68 45 75 Q50 82 58 78 Q60 76 60 75"
                      stroke="#2d5a47" stroke-width="2.5" fill="#3d6b55"
                      opacity="0.8" class="leaf leaf-medium leaf-2"/>
                <path d="M60 55 Q52 48 48 55 Q52 62 57 58 Q60 56 60 55"
                      stroke="#2d5a47" stroke-width="2" fill="#4a7a65"
                      opacity="0.75" class="leaf leaf-small leaf-3"/>
                <path d="M60 35 Q55 28 52 35 Q55 42 58 38 Q60 36 60 35"
                      stroke="#2d5a47" stroke-width="1.5" fill="#5a8a75"
                      opacity="0.7" class="leaf leaf-tiny leaf-4"/>
              </g>

              <!-- 右侧大叶子组 -->
              <g class="leaf-group-right">
                <path d="M60 95 Q75 88 82 95 Q78 102 65 98 Q60 96 60 95"
                      stroke="#2d5a47" stroke-width="3" fill="#3d6b55"
                      opacity="0.85" class="leaf leaf-large leaf-1"/>
                <path d="M60 75 Q70 68 75 75 Q70 82 62 78 Q60 76 60 75"
                      stroke="#2d5a47" stroke-width="2.5" fill="#3d6b55"
                      opacity="0.8" class="leaf leaf-medium leaf-2"/>
                <path d="M60 55 Q68 48 72 55 Q68 62 63 58 Q60 56 60 55"
                      stroke="#2d5a47" stroke-width="2" fill="#4a7a65"
                      opacity="0.75" class="leaf leaf-small leaf-3"/>
                <path d="M60 35 Q65 28 68 35 Q65 42 62 38 Q60 36 60 35"
                      stroke="#2d5a47" stroke-width="1.5" fill="#5a8a75"
                      opacity="0.7" class="leaf leaf-tiny leaf-4"/>
              </g>

              <!-- 顶部嫩芽 -->
              <ellipse cx="60" cy="5" rx="5" ry="8" fill="#1a3d2e" opacity="0.95" class="herb-bud"/>
              <ellipse cx="58" cy="7" rx="3" ry="5" fill="#2d5a47" opacity="0.8"/>

              <!-- 根系装饰 -->
              <path d="M60 130 Q55 135 50 132 M60 130 Q65 135 70 132"
                    stroke="#1a3d2e" stroke-width="2" fill="none"
                    stroke-linecap="round" opacity="0.6" class="herb-roots"/>
            </svg>

            <!-- 左侧辅助小草 -->
            <svg class="side-herb herb-left" viewBox="0 0 80 100" xmlns="http://www.w3.org/2000/svg">
              <path d="M40 90 L40 60 Q38 50 40 40 Q42 30 40 20 Q38 15 40 10"
                    stroke="#688f80" stroke-width="2.5" fill="none"
                    stroke-linecap="round" class="herb-stem-side"/>
              <path d="M40 55 Q32 50 30 55 Q32 60 38 57"
                    stroke="#688f80" stroke-width="2" fill="#7a9f8f"
                    opacity="0.7" class="leaf"/>
              <path d="M40 55 Q48 50 50 55 Q48 60 42 57"
                    stroke="#688f80" stroke-width="2" fill="#7a9f8f"
                    opacity="0.7" class="leaf"/>
              <ellipse cx="40" cy="12" rx="3" ry="5" fill="#688f80" opacity="0.8"/>
            </svg>

            <!-- 右侧辅助小草 -->
            <svg class="side-herb herb-right" viewBox="0 0 80 100" xmlns="http://www.w3.org/2000/svg">
              <path d="M40 90 L40 65 Q38 55 40 45 Q42 35 40 25 Q38 20 40 15"
                    stroke="#688f80" stroke-width="2.5" fill="none"
                    stroke-linecap="round" class="herb-stem-side"/>
              <path d="M40 60 Q33 55 31 60 Q33 65 38 62"
                    stroke="#688f80" stroke-width="2" fill="#7a9f8f"
                    opacity="0.7" class="leaf"/>
              <path d="M40 60 Q47 55 49 60 Q47 65 42 62"
                    stroke="#688f80" stroke-width="2" fill="#7a9f8f"
                    opacity="0.7" class="leaf"/>
              <ellipse cx="40" cy="17" rx="3" ry="5" fill="#688f80" opacity="0.8"/>
            </svg>

            <!-- 缠绕粒子系统 - 多层螺旋 -->
            <div class="herb-particles-container">
              <!-- 内层粒子 -->
              <div v-for="n in 30" :key="`inner-${n}`"
                   class="herb-particle herb-particle-inner"
                   :style="getHerbParticleStyle(n, 'inner')"></div>
              <!-- 外层粒子 -->
              <div v-for="n in 25" :key="`outer-${n}`"
                   class="herb-particle herb-particle-outer"
                   :style="getHerbParticleStyle(n, 'outer')"></div>
              <!-- 中层粒子 -->
              <div v-for="n in 20" :key="`mid-${n}`"
                   class="herb-particle herb-particle-mid"
                   :style="getHerbParticleStyle(n, 'mid')"></div>
            </div>

            <!-- 能量光点 -->
            <div class="herb-energy">
              <div v-for="n in 12" :key="`energy-${n}`"
                   class="energy-dot"
                   :style="getEnergyDotStyle(n)"></div>
            </div>
          </div>

          <!-- Logo文字 -->
          <div class="logo-text-wrapper">
            <span class="logo-text">岐黄</span>
            <span class="logo-divider">·</span>
            <span class="logo-highlight">AI</span>
            <span class="logo-subtitle">本草智能</span>
          </div>
        </div>
      </div>

      <!-- 中间：功能菜单 (横向排列) -->
      <nav class="nav-center">
        <button class="nav-item" @click="navigate('/chat_page')">
          <span class="nav-icon-wrapper">
            <i class="ri-chat-3-line nav-icon"></i>
          </span>
          <span class="nav-label">智能问诊</span>
          <div class="ink-stroke"></div>
          <div class="nav-glow"></div>
        </button>

        <button class="nav-item" @click="navigate('/ai_consult_wizard')">
          <span class="nav-icon-wrapper">
            <i class="ri-flask-line nav-icon"></i>
          </span>
          <span class="nav-label">流程问诊</span>
          <div class="ink-stroke"></div>
          <div class="nav-glow"></div>
        </button>

        <button class="nav-item" @click="navigate('/recommend')">
          <span class="nav-icon-wrapper">
            <i class="ri-plant-line nav-icon"></i>
          </span>
          <span class="nav-label">中药推荐</span>
          <div class="ink-stroke"></div>
          <div class="nav-glow"></div>
        </button>

        <button class="nav-item" @click="navigate('/knowledge_graph')">
          <span class="nav-icon-wrapper">
            <i class="ri-node-tree nav-icon"></i>
          </span>
          <span class="nav-label">知识图谱</span>
          <div class="ink-stroke"></div>
          <div class="nav-glow"></div>
        </button>
      </nav>

      <!-- 右侧：登录/注册 -->
      <div class="nav-right">
        <button class="login-btn" @click="handleLogin">
          <span class="login-icon">👤</span>
          <span>登录 / 注册</span>
          <i class="ri-arrow-right-s-line login-arrow"></i>
          <div class="login-shimmer"></div>
        </button>
      </div>
    </header>

    <!-- ================= 3. 主视觉区域 ================= -->
    <main class="hero-section">
      <!-- 背景本草层系统 -->
      <div class="background-herbs-layer">
        <div v-for="n in 35" :key="`bg-herb-${n}`"
             class="background-herb"
             :class="getHerbClass(n)"
             :style="getBackgroundHerbStyle(n)">
          <svg viewBox="0 0 100 130" xmlns="http://www.w3.org/2000/svg" class="herb-svg-bg">
            <!-- 类型1: 单茎多叶草 -->
            <g v-if="n % 5 === 1">
              <path d="M50 110 L50 70 Q48 60 50 50 Q52 40 50 30 Q48 20 50 15"
                    :stroke="getHerbColor(n)"
                    :stroke-width="getStrokeWidth(n)"
                    fill="none"
                    stroke-linecap="round"
                    class="herb-stem-bg"/>
              <path d="M50 75 Q42 70 38 75 Q42 80 48 77"
                    :stroke="getHerbColor(n)"
                    :fill="getHerbColorRGBA(n, 0.25)"
                    :stroke-width="getStrokeWidth(n) * 0.85"
                    :opacity="getOpacity(n)"
                    class="herb-leaf-bg"/>
              <path d="M50 75 Q58 70 62 75 Q58 80 52 77"
                    :stroke="getHerbColor(n)"
                    :fill="getHerbColorRGBA(n, 0.25)"
                    :stroke-width="getStrokeWidth(n) * 0.85"
                    :opacity="getOpacity(n)"
                    class="herb-leaf-bg"/>
              <path d="M50 55 Q45 50 42 55 Q45 60 48 57"
                    :stroke="getHerbColor(n)"
                    :fill="getHerbColorRGBA(n, 0.2)"
                    :stroke-width="getStrokeWidth(n) * 0.75"
                    :opacity="getOpacity(n)"
                    class="herb-leaf-bg"/>
              <path d="M50 55 Q55 50 58 55 Q55 60 52 57"
                    :stroke="getHerbColor(n)"
                    :fill="getHerbColorRGBA(n, 0.2)"
                    :stroke-width="getStrokeWidth(n) * 0.75"
                    :opacity="getOpacity(n)"
                    class="herb-leaf-bg"/>
              <ellipse cx="50" cy="17" :rx="2 + Math.random()" :ry="4 + Math.random()" :fill="getHerbColor(n)" :opacity="getOpacity(n) * 0.8" class="herb-bud-bg"/>
            </g>
            <!-- 类型2: 双茎草本 -->
            <g v-else-if="n % 5 === 2">
              <path d="M45 110 L45 75 Q43 65 45 55 Q47 45 45 35"
                    :stroke="getHerbColor(n)"
                    :stroke-width="getStrokeWidth(n)"
                    fill="none"
                    stroke-linecap="round"
                    class="herb-stem-bg"/>
              <path d="M55 110 L55 80 Q57 70 55 60 Q53 50 55 40"
                    :stroke="getHerbColor(n)"
                    :stroke-width="getStrokeWidth(n) * 0.9"
                    fill="none"
                    stroke-linecap="round"
                    class="herb-stem-bg"/>
              <circle cx="45" cy="38" :r="2.5 + Math.random()" :fill="getHerbColorRGBA(n, 0.3)" :opacity="getOpacity(n)" class="herb-bud-bg"/>
              <circle cx="55" cy="43" :r="2.5 + Math.random()" :fill="getHerbColorRGBA(n, 0.3)" :opacity="getOpacity(n)" class="herb-bud-bg"/>
            </g>
            <!-- 类型3: 蕨类植物 -->
            <g v-else-if="n % 5 === 3">
              <path d="M50 110 Q48 90 50 70 Q52 55 50 40 Q48 30 50 25"
                    :stroke="getHerbColor(n, 'light')"
                    :stroke-width="getStrokeWidth(n)"
                    fill="none"
                    stroke-linecap="round"
                    class="herb-stem-bg"/>
              <path d="M50 60 Q42 55 40 60 Q42 65 47 62"
                    :stroke="getHerbColor(n)"
                    :fill="getHerbColorRGBA(n, 0.2)"
                    :stroke-width="getStrokeWidth(n) * 0.7"
                    :opacity="getOpacity(n)"
                    class="herb-leaf-bg"/>
              <path d="M50 60 Q58 55 60 60 Q58 65 53 62"
                    :stroke="getHerbColor(n)"
                    :fill="getHerbColorRGBA(n, 0.2)"
                    :stroke-width="getStrokeWidth(n) * 0.7"
                    :opacity="getOpacity(n)"
                    class="herb-leaf-bg"/>
              <path d="M50 45 Q46 40 44 45 Q46 50 48 47"
                    :stroke="getHerbColor(n)"
                    :fill="getHerbColorRGBA(n, 0.2)"
                    :stroke-width="getStrokeWidth(n) * 0.7"
                    :opacity="getOpacity(n)"
                    class="herb-leaf-bg"/>
            </g>
            <!-- 类型4: 细长草 -->
            <g v-else-if="n % 5 === 4">
              <path d="M50 110 L50 60 Q49 50 50 40 Q51 30 50 25"
                    :stroke="getHerbColor(n, 'light')"
                    :stroke-width="getStrokeWidth(n) * 0.9"
                    fill="none"
                    stroke-linecap="round"
                    class="herb-stem-bg"/>
              <ellipse cx="50" cy="27" :rx="1.5 + Math.random()" :ry="3 + Math.random() * 2" :fill="getHerbColorRGBA(n, 0.3)" :opacity="getOpacity(n)" class="herb-bud-bg"/>
            </g>
            <!-- 类型5: 复合草本 -->
            <g v-else>
              <path d="M50 110 L50 75 Q48 65 50 55 Q52 45 50 35 Q48 25 50 20"
                    :stroke="getHerbColor(n)"
                    :stroke-width="getStrokeWidth(n)"
                    fill="none"
                    stroke-linecap="round"
                    class="herb-stem-bg"/>
              <path d="M50 70 Q43 65 40 70"
                    :stroke="getHerbColor(n, 'light')"
                    :stroke-width="getStrokeWidth(n) * 0.85"
                    fill="none"
                    stroke-linecap="round"
                    class="herb-stem-bg"/>
              <path d="M50 70 Q57 65 60 70"
                    :stroke="getHerbColor(n, 'light')"
                    :stroke-width="getStrokeWidth(n) * 0.85"
                    fill="none"
                    stroke-linecap="round"
                    class="herb-stem-bg"/>
              <path d="M40 70 Q38 65 36 70 Q38 75 42 72"
                    :stroke="getHerbColor(n)"
                    :fill="getHerbColorRGBA(n, 0.25)"
                    :stroke-width="getStrokeWidth(n) * 0.75"
                    :opacity="getOpacity(n)"
                    class="herb-leaf-bg"/>
              <path d="M60 70 Q62 65 64 70 Q62 75 58 72"
                    :stroke="getHerbColor(n)"
                    :fill="getHerbColorRGBA(n, 0.25)"
                    :stroke-width="getStrokeWidth(n) * 0.75"
                    :opacity="getOpacity(n)"
                    class="herb-leaf-bg"/>
            </g>
          </svg>
        </div>
      </div>

      <!-- 左侧：文字与召唤操作 -->
      <div class="text-content" :style="textParallax">
        <!-- 印章标签组 -->
        <div class="stamp-group">
          <div class="stamp stamp-primary">
            <span class="stamp-text">源于传统</span>
            <div class="stamp-border"></div>
          </div>
          <div class="stamp-connector"></div>
          <div class="stamp stamp-secondary">
            <span class="stamp-text">智于现代</span>
            <div class="stamp-border"></div>
          </div>
          <div class="stamp-decoration"></div>
        </div>

        <!-- 主标题 -->
        <h1 class="main-title">
          <span class="char-wrapper">
            <span class="char" style="animation-delay: 0.1s">悬</span>
            <span class="char-shadow" style="animation-delay: 0.1s">悬</span>
          </span>
          <span class="char-wrapper">
            <span class="char" style="animation-delay: 0.2s">壶</span>
            <span class="char-shadow" style="animation-delay: 0.2s">壶</span>
          </span>
          <span class="char-wrapper">
            <span class="char" style="animation-delay: 0.3s">济</span>
            <span class="char-shadow" style="animation-delay: 0.3s">济</span>
          </span>
          <span class="char-wrapper">
            <span class="char" style="animation-delay: 0.4s">世</span>
            <span class="char-shadow" style="animation-delay: 0.4s">世</span>
          </span>
        </h1>

        <!-- 副标题 -->
        <div class="sub-title-wrapper">
          <p class="sub-title">AI-Powered Traditional Chinese Medicine</p>
          <div class="title-underline"></div>
        </div>

        <!-- 描述文字 -->
        <div class="desc-wrapper">
          <p class="desc-line">汇集千年医案数据，融合深度学习算法。</p>
          <p class="desc-line">为您提供精准的辨证分析与本草调理建议。</p>
          <div class="desc-divider"></div>
        </div>

        <!-- 特性标签 -->
        <div class="feature-tags">
          <div class="feature-tag">
            <i class="ri-database-2-line"></i>
            <span>海量医案</span>
          </div>
          <div class="feature-tag">
            <i class="ri-brain-line"></i>
            <span>AI智能</span>
          </div>
          <div class="feature-tag">
            <i class="ri-leaf-line"></i>
            <span>本草精粹</span>
          </div>
        </div>

        <!-- 行动按钮组 -->
        <div class="cta-group">
          <button class="cta-primary cta-main" @click="navigate('/chat_page')">
            <span class="cta-icon">💊</span>
            <span class="cta-text">立即问诊</span>
            <i class="ri-pulse-line cta-arrow"></i>
            <div class="cta-ripple"></div>
            <div class="cta-glow"></div>
          </button>
          <button class="cta-primary cta-secondary" @click="navigate('/recommend')">
            <span class="cta-icon">🌿</span>
            <span class="cta-text">探索本草库</span>
            <div class="cta-ripple"></div>
          </button>
        </div>
      </div>

      <!-- 右侧：本草浮岛视觉中心 -->
      <div class="visual-content" :style="visualParallax">
        <!-- 多层装饰环 -->
        <div class="decorative-rings">
          <div class="ring ring-innermost"></div>
          <div class="ring ring-inner"></div>
          <div class="ring ring-middle"></div>
          <div class="ring ring-outer"></div>
          <div class="ring ring-outermost"></div>
        </div>

        <!-- 旋转的装饰轨道 -->
        <div class="orbit-system">
          <div class="orbit orbit-fast"></div>
          <div class="orbit orbit-slow"></div>
        </div>

        <!-- 悬浮的中药卡片组 -->
        <div class="herb-cards-container">
          <!-- 卡片1: 黄芪 -->
          <div class="herb-card card-top" @click="navigate('/recommend')">
            <div class="card-glow"></div>
            <div class="card-inner">
              <div class="card-image-wrapper">
                <img src="../../static/pictures/huangqi.png" alt="黄芪" />
                <div class="card-overlay"></div>
              </div>
              <div class="card-label">
                <span class="card-name">黄芪</span>
                <span class="card-tag">补气固表</span>
                <div class="card-property">
                  <span>性温</span>
                  <span>味甘</span>
                </div>
              </div>
            </div>
            <div class="card-particles">
              <div v-for="n in 8" :key="`card1-${n}`" class="card-particle"></div>
            </div>
          </div>

          <!-- 卡片2: 酸枣仁 -->
          <div class="herb-card card-mid" @click="navigate('/recommend')">
            <div class="card-glow"></div>
            <div class="card-inner">
              <div class="card-image-wrapper">
                <img src="../../static/pictures/suanzaoren.png" alt="酸枣仁" />
                <div class="card-overlay"></div>
              </div>
              <div class="card-label">
                <span class="card-name">酸枣仁</span>
                <span class="card-tag">养心安神</span>
                <div class="card-property">
                  <span>性平</span>
                  <span>味甘</span>
                </div>
              </div>
            </div>
            <div class="card-particles">
              <div v-for="n in 8" :key="`card2-${n}`" class="card-particle"></div>
            </div>
          </div>

          <!-- 卡片3: 当归 -->
          <div class="herb-card card-bottom" @click="navigate('/recommend')">
            <div class="card-glow"></div>
            <div class="card-inner">
              <div class="card-image-wrapper">
                <img src="../../static/pictures/danggui.png" alt="当归" />
                <div class="card-overlay"></div>
              </div>
              <div class="card-label">
                <span class="card-name">当归</span>
                <span class="card-tag">补血活血</span>
                <div class="card-property">
                  <span>性温</span>
                  <span>味甘辛</span>
                </div>
              </div>
            </div>
            <div class="card-particles">
              <div v-for="n in 8" :key="`card3-${n}`" class="card-particle"></div>
            </div>
          </div>
        </div>

        <!-- 中心能量核心 -->
        <div class="energy-core">
          <div class="core-inner"></div>
          <div class="core-pulse"></div>
        </div>
      </div>

      <!-- 装饰文字 -->
      <div class="vertical-decorations">
        <div class="vertical-deco left-deco">道法自然</div>
        <div class="vertical-deco right-deco">医者仁心</div>
      </div>
    </main>

    <!-- ================= 4. 底部装饰 ================= -->
    <footer class="home-footer">
      <div class="footer-waves">
        <div class="footer-wave"></div>
        <div class="footer-wave"></div>
      </div>
      <div class="footer-content">
        <div class="footer-text">传承千年智慧 · 融合现代科技</div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const mouseX = ref(0);
const mouseY = ref(0);
const isScrolled = ref(false);

// 预生成位置数组（避免每次渲染都重新计算）
const herbPositions = (() => {
  const positions = [];
  for (let i = 0; i < 35; i++) {
    let x, y;
    // 避开主要内容区域：左侧文字(0-45%)和右侧视觉中心(55-100%)，以及中心30-70%的垂直区域
    do {
      x = Math.random() * 100;
      y = Math.random() * 100;
    } while (
      (x > 38 && x < 62 && y > 25 && y < 75) // 避开中心区域
    );
    positions.push({ x, y, rotation: Math.random() * 360, size: 80 + Math.random() * 120 });
  }
  return positions;
})();

// 路由跳转
const navigate = (path) => {
  router.push(path);
};

// 登录点击
const handleLogin = () => {
  alert("登录模态框将在此处弹出");
};

// 滚动监听
const handleScroll = () => {
  isScrolled.value = window.scrollY > 20;
};

// 鼠标视差计算（平滑处理）
const handleMouseMove = (e) => {
  const x = (e.clientX / window.innerWidth) - 0.5;
  const y = (e.clientY / window.innerHeight) - 0.5;
  mouseX.value = mouseX.value * 0.8 + x * 0.2; // 平滑插值
  mouseY.value = mouseY.value * 0.8 + y * 0.2;
};

// 文字层视差
const textParallax = computed(() => ({
  transform: `translate(${mouseX.value * 12}px, ${mouseY.value * 12}px)`,
  transition: 'transform 0.1s ease-out'
}));

// 视觉层视差（3D景深效果）
const visualParallax = computed(() => ({
  transform: `translate(${-mouseX.value * 35}px, ${-mouseY.value * 35}px) rotateY(${mouseX.value * 5}deg)`,
  transition: 'transform 0.1s ease-out'
}));

// 全局粒子样式
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
    opacity: Math.random() * 0.5 + 0.2
  };
};

// 草的缠绕粒子样式（多层螺旋）
const getHerbParticleStyle = (n, layer) => {
  const configs = {
    inner: { radius: 18, duration: 6, offset: 0, count: 30 },
    mid: { radius: 28, duration: 8, offset: 120, count: 20 },
    outer: { radius: 40, duration: 10, offset: 240, count: 25 }
  };
  const config = configs[layer];
  const angle = ((n / config.count) * 360) + config.offset;
  const size = layer === 'inner' ? 2.5 : layer === 'mid' ? 3 : 3.5;

  return {
    '--angle': `${angle}deg`,
    '--radius': `${config.radius}px`,
    '--duration': `${config.duration}s`,
    width: `${size}px`,
    height: `${size}px`,
    animationDelay: `${n * 0.1}s`,
    opacity: layer === 'inner' ? 0.6 : layer === 'mid' ? 0.5 : 0.4
  };
};

// 能量点样式
const getEnergyDotStyle = (n) => {
  const angle = (n / 12) * 360;
  const radius = 35;
  return {
    '--angle': `${angle}deg`,
    '--radius': `${radius}px`,
    animationDelay: `${n * 0.2}s`
  };
};

// 背景草样式生成
const getBackgroundHerbStyle = (n) => {
  const pos = herbPositions[n - 1];
  const opacity = 0.23 + Math.random() * 0.08; // 0.03-0.08 非常低的透明度

  return {
    left: `${pos.x}%`,
    top: `${pos.y}%`,
    width: `${pos.size}px`,
    height: `${pos.size * 1.3}px`,
    transform: `rotate(${pos.rotation}deg)`,
    opacity: opacity,
    animationDelay: `${n * 0.3}s`,
    animationDuration: `${8 + Math.random() * 12}s`,
    '--initial-rotation': `${pos.rotation}deg`
  };
};

// 获取草的class
const getHerbClass = (n) => {
  const classes = ['herb-type-1', 'herb-type-2', 'herb-type-3', 'herb-type-4', 'herb-type-5'];
  return classes[(n - 1) % 5];
};

// 获取stroke宽度
const getStrokeWidth = (n) => {
  return 1.2 + Math.random() * 0.8;
};

// 获取颜色（hex格式）
const getHerbColor = (n, variant = 'normal') => {
  const colors = {
    normal: ['#2d5a47', '#3d6b55', '#4a7a65', '#688f80', '#5a8a75'],
    light: ['#688f80', '#7a9f8f', '#8aaf9f', '#9abfaf', '#8aaf9f']
  };
  const palette = colors[variant] || colors.normal;
  return palette[n % palette.length];
};

// 获取颜色（rgba格式）
const getHerbColorRGBA = (n, alpha) => {
  const hex = getHerbColor(n);
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
};

// 获取透明度
const getOpacity = (n) => {
  return 0.4 + Math.random() * 0.3; // 0.4-0.7
};

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
});
</script>

<style scoped>
/* ====== 引入字体和图标库 ====== */
@import url('https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=Noto+Serif+SC:wght@300;400;600;700;900&family=Cinzel:wght@400;600;700&family=ZCOOL+XiaoWei&display=swap');
@import url("https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css");

/* ====== 核心配色系统 ====== */
:root {
  --bg-base: #f7f9f4;
  --ink-green: #1a3d2e;
  --ink-green-dark: #0f281f;
  --sage-green: #2d5a47;
  --sage-green-light: #3d6b55;
  --light-green: #dcece6;
  --light-green-2: #c8ddd4;
  --gold-accent: #c5a666;
  --gold-light: #d4b877;
  --amber: #e6c98a;
  --paper-texture: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0IiBoZWlnaHQ9IjQiPgo8cmVjdCB3aWR0aD0iNCIgaGVpZ2h0PSI0IiBmaWxsPSIjZjdmOWY0Ii8+CjxyZWN0IHdpZHRoPSIxIiBoZWlnaHQ9IjEiIGZpbGw9IiNlMmU2ZTAiLz4KPC9zdmc+');
  --primary: #6fbf9a;
  --primary-dark: #2c5c4d;
}

/* ====== 全局容器 ====== */
.tcm-home {
  width: 100vw;
  min-height: 100vh;
  background-color: var(--bg-base);
  color: var(--ink-green);
  font-family: 'Noto Serif SC', serif;
  overflow-x: hidden;
  position: relative;
}

/* ====== 1. 多层次背景系统 ====== */
.bg-layer {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.paper-texture {
  background-image: var(--paper-texture);
  opacity: 0.85;
  z-index: 0;
}

/* 水墨晕染层 - 多层叠加 */
.ink-blobs {
  z-index: 1;
  filter: blur(100px);
  opacity: 0.4;
}

.blob {
  position: absolute;
  border-radius: 50%;
  animation: breathe 12s infinite ease-in-out;
}

.blob-green-1 {
  width: 70vw;
  height: 70vw;
  background: var(--light-green);
  top: -25%;
  left: -15%;
  animation-duration: 14s;
}

.blob-green-2 {
  width: 50vw;
  height: 50vw;
  background: var(--light-green-2);
  bottom: -15%;
  left: 10%;
  animation-duration: 16s;
  animation-delay: -3s;
}

.blob-gold-1 {
  width: 45vw;
  height: 45vw;
  background: rgba(197, 166, 102, 0.2);
  top: 20%;
  right: -10%;
  animation-duration: 18s;
  animation-delay: -5s;
}

.blob-gold-2 {
  width: 35vw;
  height: 35vw;
  background: rgba(212, 184, 119, 0.15);
  bottom: 10%;
  right: 5%;
  animation-duration: 15s;
  animation-delay: -7s;
}

.blob-amber {
  width: 40vw;
  height: 40vw;
  background: rgba(230, 201, 138, 0.12);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-duration: 20s;
  animation-delay: -10s;
}

/* 本草图案装饰层 */
.herb-pattern-layer {
  z-index: 1;
  opacity: 0.03;
}

.herb-pattern {
  position: absolute;
  width: 400px;
  height: 400px;
  background-image: url("data:image/svg+xml,%3Csvg width='100' height='120' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M50 110 L50 60 Q48 50 50 40 Q52 30 50 20' stroke='%231a3d2e' stroke-width='2' fill='none'/%3E%3C/svg%3E");
  background-repeat: repeat;
  animation: patternFloat 30s infinite ease-in-out;
}

.herb-pattern-1 {
  top: 10%;
  left: 5%;
  animation-duration: 35s;
}

.herb-pattern-2 {
  bottom: 15%;
  right: 8%;
  animation-duration: 40s;
  animation-delay: -10s;
}

.herb-pattern-3 {
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-duration: 45s;
  animation-delay: -20s;
}

/* 全局悬浮粒子 */
.particles {
  z-index: 2;
}

.particle {
  position: absolute;
  background: var(--gold-accent);
  border-radius: 50%;
  box-shadow: 0 0 10px rgba(197, 166, 102, 0.7), 0 0 20px rgba(197, 166, 102, 0.4);
  animation: floatUpParticle linear infinite;
}

/* 能量波纹 */
.energy-waves {
  z-index: 1;
  opacity: 0.15;
}

.wave {
  position: absolute;
  width: 200%;
  height: 200%;
  top: -50%;
  left: -50%;
  border-radius: 50%;
  border: 2px solid var(--sage-green);
  animation: waveExpand 8s infinite ease-out;
}

.wave-1 {
  animation-delay: 0s;
}

.wave-2 {
  animation-delay: 2.5s;
}

.wave-3 {
  animation-delay: 5s;
}

/* ====== 2. 导航栏系统 ====== */
.glass-nav {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 90px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 50px;
  z-index: 1000;
  background: rgba(247, 249, 244, 0.75);
  backdrop-filter: blur(20px) saturate(180%);
  border-bottom: 1px solid rgba(44, 74, 62, 0.08);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.02);
}

.glass-nav.scrolled {
  height: 75px;
  background: rgba(247, 249, 244, 0.9);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.05);
}

/* 左侧 Logo 区域 */
.nav-left {
  flex: 1;
  display: flex;
  align-items: center;
}

.logo-area {
  display: flex;
  align-items: center;
  gap: 18px;
}

/* 本草植物群容器 */
.herb-garden {
  position: relative;
  width: 70px;
  height: 85px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 5px;
}

.main-herb {
  width: 100%;
  height: 100%;
  z-index: 3;
  position: relative;
  animation: herbSwayMain 5s ease-in-out infinite;
  transform-origin: bottom center;
  filter: drop-shadow(0 2px 4px rgba(26, 61, 46, 0.15));
}

.herb-stem-main {
  filter: drop-shadow(0 1px 2px rgba(26, 61, 46, 0.2));
}

.leaf-group-left .leaf,
.leaf-group-right .leaf {
  transform-origin: 50% 50%;
  animation: leafWave 4s ease-in-out infinite;
}

.leaf-1 { animation-delay: 0s; }
.leaf-2 { animation-delay: 0.5s; }
.leaf-3 { animation-delay: 1s; }
.leaf-4 { animation-delay: 1.5s; }

.herb-bud {
  animation: budPulse 3s ease-in-out infinite;
}

.herb-roots {
  animation: rootPulse 4s ease-in-out infinite;
}

/* 侧边小草 */
.side-herb {
  position: absolute;
  width: 45px;
  height: 55px;
  z-index: 2;
  opacity: 0.7;
  animation: herbSwaySide 6s ease-in-out infinite;
  transform-origin: bottom center;
}

.herb-left {
  left: -15px;
  top: 15px;
  animation-delay: -1s;
}

.herb-right {
  right: -15px;
  top: 10px;
  animation-delay: -2s;
}

.herb-stem-side {
  filter: drop-shadow(0 1px 2px rgba(104, 143, 128, 0.2));
}

/* 缠绕粒子系统 */
.herb-particles-container {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  z-index: 1;
  pointer-events: none;
}

.herb-particle {
  position: absolute;
  border-radius: 50%;
  bottom: 5px;
  left: 50%;
  transform: translateX(-50%);
  animation: spiralUpHerb linear infinite;
}

.herb-particle-inner {
  background: var(--sage-green);
  box-shadow: 0 0 6px rgba(45, 90, 71, 0.8), 0 0 12px rgba(45, 90, 71, 0.4);
}

.herb-particle-mid {
  background: var(--sage-green-light);
  box-shadow: 0 0 8px rgba(61, 107, 85, 0.7), 0 0 16px rgba(61, 107, 85, 0.3);
}

.herb-particle-outer {
  background: var(--gold-accent);
  box-shadow: 0 0 10px rgba(197, 166, 102, 0.8), 0 0 20px rgba(197, 166, 102, 0.4);
}

/* 能量光点系统 */
.herb-energy {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  z-index: 4;
  pointer-events: none;
}

.energy-dot {
  position: absolute;
  width: 4px;
  height: 4px;
  background: var(--gold-light);
  border-radius: 50%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  box-shadow: 0 0 8px rgba(212, 184, 119, 0.9), 0 0 16px rgba(212, 184, 119, 0.5);
  animation: energyOrbit linear infinite;
}

/* Logo文字 */
.logo-text-wrapper {
  display: flex;
  align-items: baseline;
  gap: 8px;
  font-weight: 900;
  font-size: 26px;
  color: var(--ink-green);
}

.logo-text {
  font-family: 'Ma Shan Zheng', cursive;
  letter-spacing: 2px;
}

.logo-divider {
  color: var(--gold-accent);
  font-size: 20px;
  margin: 0 2px;
}

.logo-highlight {
  color: var(--gold-accent);
  font-family: 'Cinzel', serif;
  font-weight: 700;
  font-size: 28px;
}

.logo-subtitle {
  font-size: 12px;
  color: var(--sage-green);
  font-weight: 400;
  margin-left: 8px;
  letter-spacing: 1px;
  opacity: 0.8;
}

/* 中间导航菜单 */
.nav-center {
  flex: 2;
  display: flex;
  justify-content: center;
  gap: 12px;
}

.nav-item {
  position: relative;
  background: transparent;
  border: none;
  padding: 12px 24px;
  font-family: 'Noto Serif SC', serif;
  font-size: 15px;
  font-weight: 600;
  color: var(--sage-green);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 10px;
  overflow: visible;
}

.nav-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
}

.nav-icon {
  font-size: 20px;
  transition: transform 0.3s ease;
}

.nav-label {
  transition: color 0.3s ease;
}

.nav-item:hover {
  color: var(--ink-green);
  background: rgba(45, 90, 71, 0.06);
  transform: translateY(-2px);
}

.nav-item:hover .nav-icon {
  transform: scale(1.15) rotate(5deg);
}

.ink-stroke {
  position: absolute;
  bottom: 8px;
  left: 50%;
  width: 0;
  height: 3px;
  background: linear-gradient(90deg, transparent, var(--gold-accent), transparent);
  border-radius: 2px;
  transform: translateX(-50%);
  transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  opacity: 0.9;
}

.nav-item:hover .ink-stroke {
  width: 70%;
}

.nav-glow {
  position: absolute;
  inset: -2px;
  border-radius: 10px;
  background: radial-gradient(circle at center, rgba(197, 166, 102, 0.2), transparent 70%);
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: -1;
}

.nav-item:hover .nav-glow {
  opacity: 1;
}

/* 右侧登录按钮 */
.nav-right {
  flex: 1;
  display: flex;
  justify-content: flex-end;
}

.login-btn {
  position: relative;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: #fff;
  border: none;
  padding: 14px 28px;
  font-weight: 600;
  font-size: 16px;
  border-radius: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 6px 20px rgba(111, 191, 154, 0.4), 0 2px 8px rgba(111, 191, 154, 0.2);
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.login-icon {
  font-size: 18px;
}

.login-arrow {
  font-size: 20px;
  transition: transform 0.3s ease;
}

.login-shimmer {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.5s ease;
}

.login-btn:hover {
  background: linear-gradient(135deg, var(--primary-dark), #1e4a3d);
  transform: translateY(-2px) scale(1.02);
  box-shadow: 0 8px 28px rgba(111, 191, 154, 0.5), 0 4px 12px rgba(111, 191, 154, 0.3);
}

.login-btn:hover .login-arrow {
  transform: translateX(4px);
}

.login-btn:hover .login-shimmer {
  left: 100%;
}

/* ====== 3. 主视觉区域 ====== */
.hero-section {
  width: 100%;
  min-height: 100vh;
  position: relative;
  z-index: 10;
  display: flex;
  align-items: center;
  padding: 120px 8% 80px;
  gap: 60px;
}

/* ====== 背景本草层系统 ====== */
.background-herbs-layer {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  pointer-events: none;
  overflow: hidden;
}

.background-herb {
  position: absolute;
  transform-origin: bottom center;
  pointer-events: none;
  animation: backgroundHerbSway ease-in-out infinite;
  filter: blur(0.5px);
}

.herb-svg-bg {
  width: 100%;
  height: 100%;
  opacity: 1;
}

.herb-stem-bg {
  opacity: 0.6;
  filter: drop-shadow(0 0.5px 1px rgba(26, 61, 46, 0.08));
}

.herb-leaf-bg {
  transition: opacity 0.3s ease;
}

.herb-bud-bg {
  transition: opacity 0.3s ease;
}

/* 不同草类型的细微差异 */
.herb-type-1 {
  animation-name: backgroundHerbSway1;
}

.herb-type-2 {
  animation-name: backgroundHerbSway2;
}

.herb-type-3 {
  animation-name: backgroundHerbSway3;
}

.herb-type-4 {
  animation-name: backgroundHerbSway4;
}

.herb-type-5 {
  animation-name: backgroundHerbSway5;
}

/* 背景草摆动动画 - 非常轻微 */
@keyframes backgroundHerbSway {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  25% {
    transform: translateY(-2px) rotate(0.5deg);
  }
  50% {
    transform: translateY(-1px) rotate(-0.3deg);
  }
  75% {
    transform: translateY(-1.5px) rotate(0.3deg);
  }
}

@keyframes backgroundHerbSway1 {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  33% {
    transform: translateY(-1.5px) rotate(0.4deg);
  }
  66% {
    transform: translateY(-0.5px) rotate(-0.2deg);
  }
}

@keyframes backgroundHerbSway2 {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  40% {
    transform: translateY(-2px) rotate(-0.3deg);
  }
  80% {
    transform: translateY(-1px) rotate(0.3deg);
  }
}

@keyframes backgroundHerbSway3 {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  30% {
    transform: translateY(-1px) rotate(0.5deg);
  }
  60% {
    transform: translateY(-1.5px) rotate(-0.4deg);
  }
  90% {
    transform: translateY(-0.8px) rotate(0.2deg);
  }
}

@keyframes backgroundHerbSway4 {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-1.8px) rotate(0.3deg);
  }
}

@keyframes backgroundHerbSway5 {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  25% {
    transform: translateY(-1.2px) rotate(-0.4deg);
  }
  75% {
    transform: translateY(-1.5px) rotate(0.4deg);
  }
}

/* 鼠标悬停时背景草的微动效果 */
.tcm-home:hover .background-herb {
  animation-duration: 8s;
}

/* 左侧文字内容 */
.text-content {
  flex: 1;
  z-index: 20;
  max-width: 650px;
}

/* 印章组 */
.stamp-group {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 35px;
  opacity: 0;
  animation: fadeUp 1s 0.3s forwards;
}

.stamp {
  position: relative;
  border: 2px solid var(--ink-green);
  color: var(--ink-green);
  padding: 6px 16px;
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 3px;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(8px);
  transform: rotate(-2deg);
  box-shadow: 0 4px 12px rgba(26, 61, 46, 0.15);
}

.stamp-secondary {
  transform: rotate(2deg);
}

.stamp-text {
  position: relative;
  z-index: 1;
}

.stamp-border {
  position: absolute;
  inset: 2px;
  border: 1px solid var(--gold-accent);
  opacity: 0.6;
}

.stamp-connector {
  width: 40px;
  height: 2px;
  background: linear-gradient(90deg, var(--gold-accent), transparent);
  opacity: 0.7;
}

.stamp-decoration {
  width: 8px;
  height: 8px;
  background: var(--gold-accent);
  border-radius: 50%;
  opacity: 0.6;
  animation: pulse 2s ease-in-out infinite;
}

/* 主标题 */
.main-title {
  font-size: 6.5rem;
  font-weight: 900;
  margin: 0 0 25px 0;
  line-height: 1.1;
  color: var(--ink-green);
  text-shadow: 3px 3px 0px rgba(197, 166, 102, 0.25);
  position: relative;
}

.char-wrapper {
  position: relative;
  display: inline-block;
  margin-right: 8px;
}

.char {
  position: relative;
  display: inline-block;
  opacity: 0;
  transform: translateY(40px);
  animation: charReveal 1s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
  background: linear-gradient(135deg, var(--ink-green) 0%, var(--sage-green) 50%, #4a7a65 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  z-index: 2;
}

.char-shadow {
  position: absolute;
  top: 4px;
  left: 4px;
  display: inline-block;
  opacity: 0;
  transform: translateY(40px);
  animation: charReveal 1s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
  background: rgba(26, 61, 46, 0.2);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  z-index: 1;
  filter: blur(2px);
}

/* 副标题 */
.sub-title-wrapper {
  margin-bottom: 30px;
  opacity: 0;
  animation: fadeUp 1s 0.8s forwards;
  position: relative;
}

.sub-title {
  font-family: 'Cinzel', serif;
  color: var(--gold-accent);
  letter-spacing: 4px;
  font-weight: 700;
  font-size: 18px;
  margin: 0;
}

.title-underline {
  width: 120px;
  height: 2px;
  background: linear-gradient(90deg, var(--gold-accent), transparent);
  margin-top: 8px;
  animation: expandWidth 1s 1.2s forwards;
  transform-origin: left;
  width: 0;
}

/* 描述文字 */
.desc-wrapper {
  margin-bottom: 40px;
  opacity: 0;
  animation: fadeUp 1s 1s forwards;
}

.desc-line {
  font-size: 17px;
  color: #4a6659;
  line-height: 2;
  margin: 0 0 12px 0;
}

.desc-divider {
  width: 60px;
  height: 1px;
  background: var(--sage-green);
  opacity: 0.3;
  margin-top: 20px;
}

/* 特性标签 */
.feature-tags {
  display: flex;
  gap: 15px;
  margin-bottom: 45px;
  opacity: 0;
  animation: fadeUp 1s 1.2s forwards;
}

.feature-tag {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  background: rgba(45, 90, 71, 0.08);
  border: 1px solid rgba(45, 90, 71, 0.15);
  border-radius: 25px;
  font-size: 14px;
  color: var(--sage-green);
  font-weight: 500;
  transition: all 0.3s ease;
}

.feature-tag i {
  font-size: 16px;
  color: var(--gold-accent);
}

.feature-tag:hover {
  background: rgba(45, 90, 71, 0.12);
  border-color: var(--gold-accent);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(45, 90, 71, 0.15);
}

/* 行动按钮组 */
.cta-group {
  display: flex;
  gap: 20px;
  opacity: 0;
  animation: fadeUp 1s 1.4s forwards;
}

.cta-primary {
  position: relative;
  border: none;
  padding: 16px 32px;
  font-weight: 600;
  font-size: 16px;
  border-radius: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 12px;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.cta-main {
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: #fff;
  box-shadow: 0 8px 24px rgba(111, 191, 154, 0.4), 0 4px 12px rgba(111, 191, 154, 0.2);
}

.cta-secondary {
  background: rgba(255, 255, 255, 0.9);
  color: var(--ink-green);
  border: 2px solid var(--sage-green);
  box-shadow: 0 4px 16px rgba(45, 90, 71, 0.15);
}

.cta-icon {
  font-size: 20px;
}

.cta-text {
  font-size: 17px;
  letter-spacing: 1px;
}

.cta-arrow {
  font-size: 20px;
  transition: transform 0.3s ease;
}

.cta-ripple {
  position: absolute;
  width: 100px;
  height: 100px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  transform: scale(0);
  opacity: 0;
  top: 50%;
  left: 50%;
  margin-left: -50px;
  margin-top: -50px;
  transition: transform 0.6s ease, opacity 0.6s ease;
}

.cta-primary:active .cta-ripple {
  transform: scale(4);
  opacity: 0;
}

.cta-glow {
  position: absolute;
  inset: -3px;
  border-radius: 16px;
  background: radial-gradient(circle at center, rgba(111, 191, 154, 0.4), transparent 70%);
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: -1;
}

.cta-main:hover {
  background: linear-gradient(135deg, var(--primary-dark), #1e4a3d);
  transform: translateY(-3px) scale(1.02);
  box-shadow: 0 12px 32px rgba(111, 191, 154, 0.5), 0 6px 16px rgba(111, 191, 154, 0.3);
}

.cta-main:hover .cta-arrow {
  transform: translateX(5px);
}

.cta-main:hover .cta-glow {
  opacity: 1;
}

.cta-secondary:hover {
  background: rgba(255, 255, 255, 1);
  border-color: var(--gold-accent);
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(45, 90, 71, 0.2);
}

/* 右侧视觉中心 */
.visual-content {
  flex: 1;
  position: relative;
  height: 700px;
  display: flex;
  justify-content: center;
  align-items: center;
  max-width: 800px;
}

/* 装饰环系统 */
.decorative-rings {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.ring {
  position: absolute;
  border-radius: 50%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  border: 2px solid;
  opacity: 0.1;
  animation: ringPulse 8s ease-in-out infinite;
}

.ring-innermost {
  width: 200px;
  height: 200px;
  border-color: var(--sage-green);
  animation-duration: 4s;
}

.ring-inner {
  width: 320px;
  height: 320px;
  border-color: var(--sage-green-light);
  animation-duration: 6s;
  animation-delay: -1s;
}

.ring-middle {
  width: 460px;
  height: 460px;
  border-color: var(--gold-accent);
  animation-duration: 8s;
  animation-delay: -2s;
}

.ring-outer {
  width: 600px;
  height: 600px;
  border-color: var(--sage-green);
  animation-duration: 10s;
  animation-delay: -3s;
}

.ring-outermost {
  width: 750px;
  height: 750px;
  border-color: var(--gold-accent);
  animation-duration: 12s;
  animation-delay: -4s;
}

/* 轨道系统 */
.orbit-system {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.orbit {
  position: absolute;
  border-radius: 50%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  border: 1px dashed;
  opacity: 0.15;
}

.orbit-fast {
  width: 500px;
  height: 500px;
  border-color: var(--gold-accent);
  animation: spin 25s linear infinite;
}

.orbit-slow {
  width: 680px;
  height: 680px;
  border-color: var(--sage-green);
  animation: spin 45s linear infinite reverse;
}

/* 中药卡片容器 */
.herb-cards-container {
  position: relative;
  width: 100%;
  height: 100%;
}

.herb-card {
  position: absolute;
  width: 200px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(12px);
  padding: 12px;
  border-radius: 16px;
  box-shadow: 0 25px 50px rgba(44, 74, 62, 0.2), 0 10px 25px rgba(44, 74, 62, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.9);
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  animation: cardFloat 8s ease-in-out infinite;
  cursor: pointer;
  overflow: visible;
}

.herb-card:hover {
  z-index: 50;
  transform: scale(1.18) translateY(-10px) !important;
  border-color: var(--gold-accent);
  box-shadow: 0 35px 70px rgba(44, 74, 62, 0.3), 0 15px 35px rgba(44, 74, 62, 0.2);
}

.card-glow {
  position: absolute;
  inset: -5px;
  border-radius: 16px;
  background: radial-gradient(circle at center, rgba(197, 166, 102, 0.3), transparent 70%);
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: -1;
}

.herb-card:hover .card-glow {
  opacity: 1;
}

.card-inner {
  border-radius: 12px;
  overflow: hidden;
  position: relative;
}

.card-image-wrapper {
  position: relative;
  overflow: hidden;
  border-radius: 10px;
}

.card-inner img {
  width: 100%;
  height: 160px;
  object-fit: cover;
  display: block;
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.card-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom, transparent, rgba(26, 61, 46, 0.1));
  opacity: 0;
  transition: opacity 0.3s ease;
}

.herb-card:hover img {
  transform: scale(1.15);
}

.herb-card:hover .card-overlay {
  opacity: 1;
}

.card-label {
  padding: 12px 6px 8px;
  text-align: center;
}

.card-name {
  display: block;
  font-weight: 700;
  font-size: 18px;
  color: var(--ink-green);
  margin-bottom: 4px;
  letter-spacing: 1px;
}

.card-tag {
  display: block;
  font-size: 12px;
  color: var(--gold-accent);
  margin-bottom: 8px;
  font-weight: 500;
  letter-spacing: 0.5px;
}

.card-property {
  display: flex;
  justify-content: center;
  gap: 12px;
  font-size: 11px;
  color: var(--sage-green);
  opacity: 0.7;
}

.card-property span {
  padding: 2px 8px;
  background: rgba(45, 90, 71, 0.08);
  border-radius: 10px;
}

.card-particles {
  position: absolute;
  inset: 0;
  pointer-events: none;
  border-radius: 16px;
  overflow: hidden;
}

.card-particle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: var(--gold-accent);
  border-radius: 50%;
  opacity: 0;
  animation: cardParticleFloat 3s ease-in-out infinite;
}

/* 卡片定位 */
.card-top {
  top: 8%;
  right: 12%;
  animation-delay: 0s;
}

.card-top .card-particle:nth-child(1) { left: 20%; animation-delay: 0s; }
.card-top .card-particle:nth-child(2) { left: 40%; animation-delay: 0.3s; }
.card-top .card-particle:nth-child(3) { left: 60%; animation-delay: 0.6s; }
.card-top .card-particle:nth-child(4) { left: 80%; animation-delay: 0.9s; }

.card-mid {
  bottom: 28%;
  right: 5%;
  animation-delay: 2s;
}

.card-mid .card-particle:nth-child(1) { left: 15%; animation-delay: 0.2s; }
.card-mid .card-particle:nth-child(2) { left: 35%; animation-delay: 0.5s; }
.card-mid .card-particle:nth-child(3) { left: 55%; animation-delay: 0.8s; }
.card-mid .card-particle:nth-child(4) { left: 75%; animation-delay: 1.1s; }

.card-bottom {
  bottom: 8%;
  left: 8%;
  animation-delay: 4s;
}

.card-bottom .card-particle:nth-child(1) { left: 25%; animation-delay: 0.1s; }
.card-bottom .card-particle:nth-child(2) { left: 45%; animation-delay: 0.4s; }
.card-bottom .card-particle:nth-child(3) { left: 65%; animation-delay: 0.7s; }
.card-bottom .card-particle:nth-child(4) { left: 85%; animation-delay: 1s; }

/* 能量核心 */
.energy-core {
  position: absolute;
  width: 120px;
  height: 120px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1;
}

.core-inner {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(197, 166, 102, 0.2), transparent);
  animation: corePulse 4s ease-in-out infinite;
}

.core-pulse {
  position: absolute;
  inset: -20px;
  border-radius: 50%;
  border: 2px solid var(--gold-accent);
  opacity: 0.3;
  animation: corePulseRing 3s ease-in-out infinite;
}

/* 竖排装饰字 */
.vertical-decorations {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.vertical-deco {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  writing-mode: vertical-rl;
  font-size: 24px;
  font-weight: 900;
  letter-spacing: 25px;
  color: var(--sage-green);
  opacity: 0.25;
  font-family: 'Ma Shan Zheng', cursive;
}

.left-deco {
  left: 20px;
  animation: decoFloat 6s ease-in-out infinite;
}

.right-deco {
  right: 20px;
  animation: decoFloat 8s ease-in-out infinite reverse;
}

/* ====== 4. 底部装饰 ====== */
.home-footer {
  position: relative;
  width: 100%;
  height: 120px;
  z-index: 5;
  margin-top: -80px;
}

.footer-waves {
  position: absolute;
  width: 100%;
  height: 100%;
  bottom: 0;
  overflow: hidden;
}

.footer-wave {
  position: absolute;
  width: 200%;
  height: 100%;
  bottom: 0;
  background: linear-gradient(180deg, transparent, rgba(26, 61, 46, 0.03));
  border-radius: 50% 50% 0 0 / 100% 100% 0 0;
  animation: waveMove 10s ease-in-out infinite;
}

.footer-wave:nth-child(2) {
  animation-delay: -5s;
  opacity: 0.5;
}

.footer-content {
  position: relative;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1;
}

.footer-text {
  font-size: 14px;
  color: var(--sage-green);
  opacity: 0.6;
  letter-spacing: 3px;
  font-weight: 400;
}

/* ====== 动画 Keyframes ====== */
@keyframes breathe {
  from { transform: scale(1); }
  to { transform: scale(1.15); }
}

@keyframes floatUpParticle {
  from {
    transform: translateY(110vh) rotate(0deg);
    opacity: 0;
  }
  15% {
    opacity: 0.8;
  }
  85% {
    opacity: 0.8;
  }
  to {
    transform: translateY(-10vh) rotate(360deg);
    opacity: 0;
  }
}

@keyframes patternFloat {
  0%, 100% { transform: translate(0, 0) rotate(0deg); }
  33% { transform: translate(20px, -20px) rotate(5deg); }
  66% { transform: translate(-20px, 20px) rotate(-5deg); }
}

@keyframes waveExpand {
  from {
    transform: scale(0);
    opacity: 0.8;
  }
  to {
    transform: scale(1);
    opacity: 0;
  }
}

@keyframes herbSwayMain {
  0%, 100% {
    transform: rotate(-2deg) translateY(0);
  }
  25% {
    transform: rotate(1.5deg) translateY(-3px);
  }
  50% {
    transform: rotate(-1deg) translateY(-1px);
  }
  75% {
    transform: rotate(1deg) translateY(-2px);
  }
}

@keyframes herbSwaySide {
  0%, 100% {
    transform: rotate(-1deg) translateY(0);
    opacity: 0.7;
  }
  50% {
    transform: rotate(1deg) translateY(-2px);
    opacity: 0.8;
  }
}

@keyframes leafWave {
  0%, 100% {
    transform: rotate(0deg) scale(1);
  }
  50% {
    transform: rotate(8deg) scale(1.08);
  }
}

@keyframes budPulse {
  0%, 100% {
    opacity: 0.95;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.15);
  }
}

@keyframes rootPulse {
  0%, 100% {
    opacity: 0.6;
  }
  50% {
    opacity: 0.8;
  }
}

@keyframes spiralUpHerb {
  0% {
    transform: translateX(-50%) translateY(80px) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 0.9;
  }
  25% {
    transform: translateX(calc(-50% + 10px)) translateY(60px) rotate(90deg);
    opacity: 0.9;
  }
  50% {
    transform: translateX(calc(-50% + 15px)) translateY(40px) rotate(180deg);
    opacity: 0.9;
  }
  75% {
    transform: translateX(calc(-50% + 10px)) translateY(20px) rotate(270deg);
    opacity: 0.9;
  }
  90% {
    opacity: 0.9;
  }
  100% {
    transform: translateX(calc(-50% - 15px)) translateY(-80px) rotate(360deg);
    opacity: 0;
  }
}
@keyframes energyOrbit {
  0% {
    transform: translate(-50%, -50%) translateX(35px) rotate(0deg);
  }
  100% {
    transform: translate(-50%, -50%) translateX(35px) rotate(360deg);
  }
}


@keyframes spin {
  100% { transform: translate(-50%, -50%) rotate(360deg); }
}

@keyframes ringPulse {
  0%, 100% {
    opacity: 0.1;
    transform: translate(-50%, -50%) scale(1);
  }
  50% {
    opacity: 0.2;
    transform: translate(-50%, -50%) scale(1.05);
  }
}

@keyframes cardFloat {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(1deg);
  }
}

@keyframes cardParticleFloat {
  0% {
    bottom: 0;
    opacity: 0;
    transform: translateX(0);
  }
  20% {
    opacity: 1;
  }
  80% {
    opacity: 1;
  }
  100% {
    bottom: 100%;
    opacity: 0;
    transform: translateX(20px);
  }
}

@keyframes corePulse {
  0%, 100% {
    opacity: 0.3;
    transform: scale(1);
  }
  50% {
    opacity: 0.5;
    transform: scale(1.1);
  }
}

@keyframes corePulseRing {
  0% {
    transform: scale(1);
    opacity: 0.3;
  }
  50% {
    transform: scale(1.3);
    opacity: 0.1;
  }
  100% {
    transform: scale(1);
    opacity: 0.3;
  }
}

@keyframes decoFloat {
  0%, 100% {
    transform: translateY(-50%) translateX(0);
  }
  50% {
    transform: translateY(-50%) translateX(10px);
  }
}

@keyframes waveMove {
  0% {
    transform: translateX(-50%);
  }
  50% {
    transform: translateX(-30%);
  }
  100% {
    transform: translateX(-50%);
  }
}

@keyframes charReveal {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes expandWidth {
  from { width: 0; }
  to { width: 120px; }
}

@keyframes pulse {
  0%, 100% {
    opacity: 0.6;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.2);
  }
}

/* ====== 响应式设计 ====== */
@media (max-width: 1400px) {
  .hero-section {
    padding: 120px 6% 80px;
    gap: 50px;
  }

  .main-title {
    font-size: 5.5rem;
  }

  .visual-content {
    height: 600px;
  }
}

@media (max-width: 1200px) {
  .glass-nav {
    padding: 0 40px;
  }

  .nav-item {
    padding: 10px 18px;
    font-size: 14px;
  }

  .nav-label {
    display: none;
  }

  .main-title {
    font-size: 4.5rem;
  }

  .hero-section {
    flex-direction: column;
    text-align: center;
    padding-top: 140px;
  }

  .text-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    max-width: 100%;
  }

  .visual-content {
    width: 100%;
    height: 500px;
    margin-top: 50px;
  }

  /* 响应式 - 减少背景草数量 */
  .background-herbs-layer .background-herb:nth-child(n+26) {
    display: none;
  }
}

@media (max-width: 768px) {
  .glass-nav {
    height: 75px;
    padding: 0 20px;
  }

  .herb-garden {
    width: 50px;
    height: 60px;
  }

  .logo-text-wrapper {
    font-size: 18px;
  }

  .logo-highlight {
    font-size: 20px;
  }

  .logo-subtitle {
    display: none;
  }

  .main-title {
    font-size: 3.5rem;
  }

  .nav-center {
    gap: 8px;
  }

  .nav-item {
    padding: 8px 12px;
  }

  .login-btn {
    padding: 10px 18px;
    font-size: 14px;
  }

  .stamp-group {
    flex-wrap: wrap;
    justify-content: center;
  }

  .feature-tags {
    flex-wrap: wrap;
    justify-content: center;
  }

  .cta-group {
    flex-direction: column;
    width: 100%;
  }

  .cta-primary {
    width: 100%;
    justify-content: center;
  }

  /* 移动端进一步减少背景草 */
  .background-herbs-layer .background-herb:nth-child(n+16) {
    display: none;
  }

  .background-herb {
    opacity: 0.02 !important;
  }
}
</style>