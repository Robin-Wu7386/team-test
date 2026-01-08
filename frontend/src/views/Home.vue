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

        <button class="nav-item" @click="navigate('/comments')">
          <span class="nav-icon-wrapper">
            <i class="ri-chat-smile-2-line nav-icon"></i>
          </span>
          <span class="nav-label">评论区</span>
          <div class="ink-stroke"></div>
          <div class="nav-glow"></div>
        </button>
      </nav>

      <!-- 右侧：登录/注册 -->
      <div class="nav-right">
        <div v-if="isLoggedIn" class="user-entry" @click="toggleUserMenu">
          <div class="avatar">{{ (currentUser.username || 'U').slice(0, 1).toUpperCase() }}</div>
          <div class="user-meta">
            <span class="user-name">{{ currentUser.username }}</span>
            <span class="user-phone">{{ currentUser.phonenumber }}</span>
          </div>
          <i class="ri-arrow-down-s-line user-arrow"></i>

          <div v-if="showUserMenu" class="user-menu" @click.stop>
            <button class="menu-action" @click="goProfile">个人中心</button>
            <button class="menu-action" @click="goMyComments">我的评论</button>
            <button class="menu-action danger" @click="handleLogout">退出登录</button>
          </div>
        </div>
        <button v-else class="login-btn" @click="navigate('/login')">
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
    <!-- ================= 4. 中药非遗传承人展示模块 ================= -->
<section class="heritage-section">
  <!-- 板块标题区（延续国风样式） -->
  <div class="heritage-title">
    <h2>国药非遗 · 匠人传承</h2>
    <p>守护中药古法技艺的传承者</p>
  </div>

  <!-- 传承人卡片容器（响应式网格布局，贴合页面风格） -->
  <div class="heritage-card-container">
    <!-- 遍历传承人数据生成卡片 -->
    <div
      class="heritage-card"
      v-for="(inheritor, index) in inheritorList"
      :key="index"
      @click="showInheritorDetail(inheritor)"
    >
      <!-- 传承人头像/技艺场景图 -->
      <img
        :src="inheritor.imgUrl"
        :alt="`${inheritor.name}-${inheritor.project}`"
        class="card-img"
      >
      <!-- 卡片内容区 -->
      <div class="card-content">
        <div class="card-name">
          {{ inheritor.name }}
          <span class="card-project">{{ inheritor.project }}</span>
        </div>
        <div class="card-tag">{{ inheritor.tag }}</div>
        <div class="card-desc">{{ inheritor.desc }}</div>
      </div>
    </div>
  </div>

  <!-- 传承人详情弹窗（点击卡片显示，贴合国风视觉） -->
  <div class="detail-modal" v-if="showModal" @click.self="closeModal">
    <div class="modal-content">
      <div class="modal-close" @click="closeModal">×</div>
      <img :src="currentInheritor.imgUrl" :alt="currentInheritor.name" class="modal-img">
      <div class="modal-info">
        <h3>{{ currentInheritor.name }} - {{ currentInheritor.project }}</h3>
        <p class="modal-tag">{{ currentInheritor.tag }}</p>
        <p class="modal-desc">{{ currentInheritor.detailDesc }}</p>
      </div>
    </div>
  </div>
</section>
    <!-- ================= 5. 道地药材产地分布 - 高德地图模块 ================= -->
<!-- 道地药材产地分布模块 -->
<section class="herb-distribution-section">
  <!-- 原有标题区 -->
  <div class="distribution-title-wrapper">
    <h2 class="distribution-main-title">道地药材 · 产地分布</h2>
    <p class="distribution-subtitle">探索传统中药材的核心产区</p>
    <div class="title-divider"></div>
    <!-- 新增：操作按钮 -->
    <button class="add-herb-btn" @click="openHerbForm('add')">
      <i class="ri-add-line"></i>
      <span>新增产地</span>
    </button>
  </div>

  <!-- 原有地图容器和筛选面板 -->
  <div class="map-container" id="herbMap"></div>
  <div class="herb-filter-panel">
    <!-- 原有筛选内容 -->
    <div class="filter-title">
      <i class="ri-map-pin-line"></i>
      <span>核心产区筛选</span>
    </div>
    <div class="filter-tags">
      <button
        v-for="(region, idx) in herbRegions"
        :key="idx"
        class="filter-tag"
        :class="{ active: activeRegion === region.name }"
        @click="filterHerbRegion(region.name)"
      >
        {{ region.name }}
      </button>
    </div>
    <div class="herb-tip">
      <i class="ri-information-line"></i>
      <span>点击地图标记查看/编辑/删除药材详情</span>
    </div>
  </div>

  <!-- 新增：药材产地增删改查表单弹窗 -->
  <div class="herb-form-modal" v-if="showHerbForm" @click.self="closeHerbForm">
    <div class="modal-inner">
      <div class="modal-header">
        <h3>{{ formType === 'add' ? '新增药材产地' : '编辑药材产地' }}</h3>
        <span class="modal-close" @click="closeHerbForm">×</span>
      </div>
      <div class="modal-form">
        <div class="form-item">
          <label>所属产区</label>
          <select v-model="currentHerb.region" required>
            <option v-for="(region, idx) in herbRegions.slice(1)" :key="idx" :value="region.name">
              {{ region.name }}
            </option>
          </select>
        </div>
        <div class="form-item">
          <label>经度</label>
          <input type="number" step="0.01" v-model="currentHerb.lnglat[0]" required placeholder="如：104.06">
        </div>
        <div class="form-item">
          <label>纬度</label>
          <input type="number" step="0.01" v-model="currentHerb.lnglat[1]" required placeholder="如：30.67">
        </div>
        <div class="form-item">
          <label>药材名称</label>
          <input type="text" v-model="currentHerb.name" required placeholder="如：川芎">
        </div>
        <div class="form-item">
          <label>药材别名</label>
          <input type="text" v-model="currentHerb.alias" placeholder="如：芎藭、小叶川芎">
        </div>
        <div class="form-item">
          <label>功效描述</label>
          <textarea v-model="currentHerb.efficacy" required placeholder="如：活血行气，祛风止痛"></textarea>
        </div>
        <div class="form-item">
          <label>道地特征</label>
          <textarea v-model="currentHerb.feature" placeholder="如：四川都江堰特产，个大饱满，香气浓郁"></textarea>
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn-cancel" @click="closeHerbForm">取消</button>
        <button class="btn-confirm" @click="submitHerbForm" :disabled="!currentHerb.name || !currentHerb.efficacy">
          {{ formType === 'add' ? '新增保存' : '编辑保存' }}
        </button>
      </div>
    </div>
  </div>

  <!-- 新增：删除确认弹窗 -->
  <div class="delete-confirm-modal" v-if="showDeleteConfirm" @click.self="closeDeleteConfirm">
    <div class="delete-modal-inner">
      <h3>确认删除</h3>
      <p>是否确定删除「{{ currentHerb.name }}」这个药材产地？删除后不可恢复！</p>
      <div class="delete-btn-group">
        <button class="btn-cancel" @click="closeDeleteConfirm">取消</button>
        <button class="btn-delete" @click="confirmDeleteHerb">确认删除</button>
      </div>
    </div>
  </div>
</section>

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
import { useUserStore } from '../stores/user';

const router = useRouter();
const userStore = useUserStore();
const mouseX = ref(0);
const mouseY = ref(0);
const isScrolled = ref(false);
const showUserMenu = ref(false);

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

const isLoggedIn = computed(() => userStore.isLoggedIn);
const currentUser = computed(() => userStore.userInfo || {});

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value;
};

const goProfile = () => {
  showUserMenu.value = false;
  if (!isLoggedIn.value) {
    router.push('/login');
    return;
  }
  router.push('/profile');
};

const goMyComments = () => {
  showUserMenu.value = false;
  router.push({ path: '/comments', query: { tab: 'mine' } });
};

const handleLogout = () => {
  userStore.logout();
  showUserMenu.value = false;
  router.push('/login');
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

// ---------------- 高德地图改造：支持增删改查 ----------------
const AMapKey = 'a51d346dda9ace47e9b2397d91f3a6aa';
const mapInstance = ref(null);
const activeRegion = ref('全部');

// 1. 动态响应式数据（替代原有静态数据，可从数据库拉取）
// 1. 动态响应式数据（替代原有静态数据，可从数据库拉取）
const herbRegions = ref([
  {
    name: '全部',
    herbs: []
  },
  {
    name: '四川',
    herbs: [
      {
        id: 1, // 新增：唯一标识（数据库主键）
        lnglat: [104.06, 30.67],
        name: '川芎',
        alias: '芎藭、小叶川芎',
        efficacy: '活血行气，祛风止痛',
        feature: '四川都江堰特产',
        region: '四川' // 新增：关联产区
      },
      {
        id: 2,
        lnglat: [103.73, 30.05],
        name: '黄连',
        alias: '川连、味连',
        efficacy: '清热燥湿，泻火解毒',
        feature: '四川雅连为特有',
        region: '四川'
      },
      {
        id: 12,
        lnglat: [105.50, 30.67],
        name: '贝母',
        alias: '川贝母、浙贝母',
        efficacy: '清热润肺，化痰止咳',
        feature: '四川川贝母颗粒小而坚实',
        region: '四川'
      }
    ]
  },
  {
    name: '云南',
    herbs: [
      {
        id: 3,
        lnglat: [102.71, 25.04],
        name: '三七',
        alias: '田七、金不换',
        efficacy: '散瘀止血，消肿定痛',
        feature: '云南文山三七为道地',
        region: '云南'
      },
      {
        id: 4,
        lnglat: [99.90, 25.88],
        name: '重楼',
        alias: '七叶一枝花',
        efficacy: '清热解毒，消肿止痛',
        feature: '云南滇重楼为道地',
        region: '云南'
      },
      {
        id: 14,
        lnglat: [102.71, 25.04],
        name: '茯苓',
        alias: '云茯苓、白茯苓',
        efficacy: '利水渗湿，健脾宁心',
        feature: '云南云茯苓质地坚实',
        region: '云南'
      }
    ]
  },
  {
    name: '安徽',
    herbs: [
      { id: 5, lnglat: [117.28, 31.86], name: '白芍', alias: '亳芍', efficacy: '养血调经，敛阴止汗', feature: '安徽亳州白芍条粗长', region: '安徽' },
      { id: 6, lnglat: [118.30, 30.56], name: '木瓜', alias: '宣木瓜', efficacy: '舒筋活络，和胃化湿', feature: '安徽宣州木瓜肉厚味酸', region: '安徽' }
    ]
  },
  {
    name: '甘肃',
    herbs: [
      { id: 7, lnglat: [103.82, 36.05], name: '当归', alias: '秦归、云归', efficacy: '补血活血，调经止痛', feature: '甘肃岷县当归油润', region: '甘肃' },
      { id: 8, lnglat: [105.15, 35.48], name: '黄芪', alias: '黄耆、北芪', efficacy: '补气升阳，固表止汗', feature: '甘肃陇西黄芪条粗', region: '甘肃' }
    ]
  },
  {
    name: '山西',
    herbs: [
      { id: 9, lnglat: [112.55, 37.87], name: '党参', alias: '潞党参、台党参', efficacy: '补中益气，健脾益肺', feature: '山西潞党参根条粗壮', region: '山西' }
    ]
  },
  {
    name: '宁夏',
    herbs: [
      { id: 10, lnglat: [106.27, 38.47], name: '枸杞', alias: '枸杞子、西枸杞', efficacy: '滋补肝肾，益精明目', feature: '宁夏中宁枸杞粒大肉厚', region: '宁夏' }
    ]
  },
  {
    name: '河南',
    herbs: [
      { id: 11, lnglat: [113.27, 34.76], name: '山药', alias: '怀山药、淮山药', efficacy: '补脾养胃，生津益肺', feature: '河南焦作怀山药质地细腻', region: '河南' }
    ]
  },
  {
    name: '浙江',
    herbs: [
      { id: 12, lnglat: [120.19, 30.26], name: '贝母', alias: '川贝母、浙贝母', efficacy: '清热润肺，化痰止咳', feature: '浙江浙贝母鳞茎肥厚', region: '浙江' },
      { id: 13, lnglat: [119.64, 30.05], name: '白术', alias: '于术、冬术', efficacy: '健脾益气，燥湿利水', feature: '浙江于潜白术个大质坚', region: '浙江' }
    ]
  },
  {
    name: '内蒙古',
    herbs: [
      { id: 15, lnglat: [111.65, 40.82], name: '甘草', alias: '甜草、国老', efficacy: '益气补中，清热解毒', feature: '内蒙古甘草条粗色红', region: '内蒙古' }
    ]
  }
]);

// 合并全部产地数据（动态更新）
const mergeAllHerbs = () => {
  herbRegions.value[0].herbs = herbRegions.value.slice(1).reduce((total, item) => {
    total.push(...item.herbs);
    return total;
  }, []);
};
// 初始化合并
mergeAllHerbs();

// 2. 表单相关响应式数据
const showHerbForm = ref(false); // 表单弹窗显示状态
const showDeleteConfirm = ref(false); // 删除确认弹窗状态
const formType = ref('add'); // add:新增 / edit:编辑
const currentHerb = ref({
  id: '',
  lnglat: [0, 0],
  name: '',
  alias: '',
  efficacy: '',
  feature: '',
  region: herbRegions.value[1]?.name || '四川'
});

// 3. 打开表单弹窗（区分新增/编辑）
const openHerbForm = (type, herb = null) => {
  formType.value = type;
  showHerbForm.value = true;
  // 禁用页面滚动
  document.body.style.overflow = 'hidden';
  // 重置/赋值表单数据
  if (type === 'add') {
    currentHerb.value = {
      id: Date.now(), // 临时ID，后端保存后替换为数据库ID
      lnglat: [108.95, 34.27], // 默认中国中心点
      name: '',
      alias: '',
      efficacy: '',
      feature: '',
      region: herbRegions.value[1]?.name || '四川'
    };
  } else if (type === 'edit' && herb) {
    currentHerb.value = { ...herb }; // 深拷贝编辑对象
  }
};

// 4. 关闭表单弹窗
const closeHerbForm = () => {
  showHerbForm.value = false;
  document.body.style.overflow = 'auto';
};

// 5. 关闭删除确认弹窗
const closeDeleteConfirm = () => {
  showDeleteConfirm.value = false;
};

// 6. 提交表单（新增/编辑）
const submitHerbForm = async () => {
  try {
    if (formType.value === 'add') {
      // 调用新增接口，持久化到数据库
      const res = await addHerbApi(currentHerb.value);
      if (res.success) {
        // 找到对应产区，添加数据
        const targetRegion = herbRegions.value.find(item => item.name === currentHerb.value.region);
        if (targetRegion) {
          targetRegion.herbs.push({ ...currentHerb.value, id: res.data.id }); // 替换为数据库返回的ID
          mergeAllHerbs(); // 重新合并全部数据
          renderHerbMarkers(herbRegions.value[0].herbs); // 重新渲染地图
        }
      }
    } else if (formType.value === 'edit') {
      // 调用编辑接口，更新数据库
      const res = await editHerbApi(currentHerb.value);
      if (res.success) {
        // 找到对应产区和药材，更新数据
        const targetRegion = herbRegions.value.find(item => item.name === currentHerb.value.region);
        if (targetRegion) {
          const herbIndex = targetRegion.herbs.findIndex(h => h.id === currentHerb.value.id);
          if (herbIndex > -1) {
            targetRegion.herbs[herbIndex] = { ...currentHerb.value };
            mergeAllHerbs(); // 重新合并全部数据
            renderHerbMarkers(herbRegions.value[0].herbs); // 重新渲染地图
          }
        }
      }
    }
    closeHerbForm(); // 关闭表单
    alert(`${formType.value === 'add' ? '新增' : '编辑'}成功！`);
  } catch (error) {
    console.error('提交失败：', error);
    alert(`${formType.value === 'add' ? '新增' : '编辑'}失败，请重试！`);
  }
};

// 7. 打开删除确认弹窗
const openDeleteConfirm = (herb) => {
  currentHerb.value = { ...herb };
  showDeleteConfirm.value = true;
  document.body.style.overflow = 'hidden';
};

// 8. 确认删除
const confirmDeleteHerb = async () => {
  try {
    // 调用删除接口，删除数据库数据
    const res = await deleteHerbApi(currentHerb.value.id);
    if (res.success) {
      // 找到对应产区，删除数据
      const targetRegion = herbRegions.value.find(item => item.name === currentHerb.value.region);
      if (targetRegion) {
        targetRegion.herbs = targetRegion.herbs.filter(h => h.id !== currentHerb.value.id);
        mergeAllHerbs(); // 重新合并全部数据
        renderHerbMarkers(herbRegions.value[0].herbs); // 重新渲染地图
      }
    }
    closeDeleteConfirm(); // 关闭删除弹窗
    alert('删除成功！');
  } catch (error) {
    console.error('删除失败：', error);
    alert('删除失败，请重试！');
  }
};

// 9. 封装增删改查API（对接后端数据库，此处为模拟接口，可替换为真实接口）
// 新增药材
const addHerbApi = (herb) => {
  // 模拟后端请求，实际项目中替换为axios/fetch
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        success: true,
        data: { id: herb.id || Date.now() } // 数据库返回的主键ID
      });
    }, 500);
  });
};

// 编辑药材
const editHerbApi = (herb) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ success: true });
    }, 500);
  });
};

// 删除药材
const deleteHerbApi = (herbId) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ success: true });
    }, 500);
  });
};

// 10. 改造渲染标记方法（添加编辑/删除事件）
const renderHerbMarkers = (herbs) => {
  if (!mapInstance.value) return;
  mapInstance.value.clearMap();

  herbs.forEach(herb => {
    // 自定义标记图标（原有代码）
    const markerIcon = new window.AMap.Icon({
      size: new window.AMap.Size(36, 36),
      image: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzYiIGhlaWdodD0iMzYiIHZpZXdCb3g9IjAgMCAzNiAzNiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48Y2lyY2xlIGN4PSIxOCIgY3k9IjE4IiByPSIxMCIgZmlsbD0iIzJkNWE0NyIgc3Ryb2tlPSIjMWEzZDJlIiBzdHJva2Utd2lkdGg9IjEuNSIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+PHBhdGggZD0iTTE4IDhDMTEuMzcgOCA2IDEzLjM3IDYgMjBDNiAyNi42MyAxMS4zNyAzMiAxOCAzMkMyNC42MyAzMiAzMCAyNi42MyAzMCAyMEMzMCAxMy4zNyAyNC42MyA4IDE4IDhNMTggMjZDMTEuMzkgMjYgNiAyMC42MSA2IDE0QzYgNy4zOSAxMS4zOSAyIDE4IDJDMjQuNjEgMiAzMCA3LjM5IDMwIDE0QzMwIDIwLjYxIDI0LjYxIDI2IDE4IDI2WiIgZmlsbD0iI2NmZmNmYyIgc3Ryb2tlPSIjMWEzZDJlIiBzdHJva2Utd2lkdGg9IjEuNSIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+PC9zdmc+',
      imageSize: new window.AMap.Size(36, 36),
      imageOffset: new window.AMap.Pixel(0, 0)
    });

    // 创建标记点（原有代码）
    const marker = new window.AMap.Marker({
      position: herb.lnglat,
      icon: markerIcon,
      offset: new window.AMap.Pixel(-18, -18),
      animation: 'AMAP_ANIMATION_DROP'
    });

    // 改造信息窗口：添加编辑/删除按钮
const infoWindow = new window.AMap.InfoWindow({
  content: `
    <div class="herb-info-window-refined">
      <!-- 顶部：名称+道地印章 -->
      <div class="info-top">
        <h3 class="info-name-refined">${herb.name}</h3>
        <div class="seal-mark">道地</div>
      </div>

      <!-- 生境分布：中式分隔线+文字 -->
      <div class="info-habitat-refined">
        <span class="habitat-label">生境分布</span>
        <span class="habitat-value">${herb.region} · ${herb.feature}</span>
      </div>

      <!-- 操作按钮：悬浮式水墨按钮 -->
      <div class="info-ops-refined">
        <button class="btn-edit-refined" onclick="window.editHerb(${JSON.stringify(herb).replace(/"/g, '&quot;')})">
          <i class="ri-edit-2-line"></i>
          <span>编辑</span>
        </button>
        <button class="btn-del-refined" onclick="window.deleteHerb(${JSON.stringify(herb).replace(/"/g, '&quot;')})">
          <i class="ri-delete-bin-line"></i>
          <span>删除</span>
        </button>
      </div>
    </div>
  `,
  offset: new window.AMap.Pixel(0, -20),
  closeWhenClickMap: true
});

    // 标记点点击事件（原有代码）
    marker.on('click', () => {
      infoWindow.open(mapInstance.value, herb.lnglat);
      marker.setAnimation('AMAP_ANIMATION_BOUNCE');
      setTimeout(() => {
        marker.setAnimation(null);
      }, 1500);
    });

    mapInstance.value.add(marker);
  });

  // 挂载全局方法，供信息窗口调用
  window.editHerb = (herb) => {
    openHerbForm('edit', herb);
  };
  window.deleteHerb = (herb) => {
    currentHerb.value = { ...herb };
    showDeleteConfirm.value = true;
    document.body.style.overflow = 'hidden';
  };
};

// 保留原有筛选方法
const filterHerbRegion = (regionName) => {
  activeRegion.value = regionName;
  const targetRegion = herbRegions.value.find(item => item.name === regionName);
  if (targetRegion) {
    renderHerbMarkers(targetRegion.herbs);
    if (regionName === '全部') {
      mapInstance.value.setCenter([108.95, 34.27]);
      mapInstance.value.setZoom(5);
    } else {
      const centerLnglat = targetRegion.herbs[0].lnglat;
      mapInstance.value.setCenter(centerLnglat);
      mapInstance.value.setZoom(8);
    }
  }
};

// 保留原有地图加载和初始化方法
const loadAMap = () => {
  return new Promise((resolve, reject) => {
    if (window.AMap) {
      resolve(window.AMap);
      return;
    }
    const script = document.createElement('script');
    script.src = `https://webapi.amap.com/maps?v=2.0&key=${AMapKey}&callback=initAMap`;
    script.type = 'text/javascript';
    script.async = true;
    window.initAMap = resolve;
    script.onerror = reject;
    document.head.appendChild(script);
  });
};

const initMap = async () => {
  try {
    await loadAMap();
    mapInstance.value = new window.AMap.Map('herbMap', {
      zoom: 5,
      center: [108.95, 34.27],
      resizeEnable: true,
      mapStyle: 'amap://styles/light',
      features: ['bg', 'road', 'building', 'point'],
      zoomEnable: true,
      dragEnable: true,
      scrollWheel: true
    });

    mapInstance.value.addControl(new window.AMap.Scale({ position: 'bottom-right' }));
    mapInstance.value.addControl(new window.AMap.Zoom({ position: 'bottom-right' }));

    renderHerbMarkers(herbRegions.value[0].herbs);
  } catch (error) {
    console.error('高德地图加载失败:', error);
  }
};

// 挂载时初始化
onMounted(() => {
  window.addEventListener('scroll', handleScroll);
  setTimeout(initMap, 500);
});

// ================= 非遗传承人核心数据与方法 =================
const showModal = ref(false); // 控制详情弹窗显示/隐藏
const currentInheritor = ref({}); // 存储当前选中的传承人信息
// 非遗传承人列表数据（可根据实际需求扩展）
const inheritorList = ref([
  {
    name: "王孝涛",
    project: "中药炮制技术",
    tag: "炮制学科奠基人 | 国家级非遗第一批传承人",
    desc: "编撰《中药炮制经验集成》，规范传统饮片工艺，奠定中药炮制学科体系。",
    detailDesc: "王孝涛先生是我国著名中药炮制专家，毕生致力于中药炮制技艺的整理、研究与传承。他牵头编撰了多部中药炮制经典著作，系统梳理了全国各地区的炮制经验，推动中药炮制从传统经验向现代科学标准化发展，培养了大批中药炮制专业人才。",
    imgUrl: "/static/pictures/王孝涛.jpg"// 可替换为真实图片地址
  },
  {
    name: "肖永庆",
    project: "中药炮制技术",
    tag: "炮制与药性研究专家 | 第六批国家级非遗传承人",
    desc: "提出“炮制与药性相关性”研究范式，完善饮片质量标准体系。",
    detailDesc: "肖永庆长期从事中药炮制工艺与质量标准研究，聚焦中药炮制前后药性变化规律，建立了多项中药饮片质量控制方法，推动传统中药炮制技艺与现代检测技术相结合，为中药饮片的规范化生产和临床安全用药提供了重要支撑。",
   imgUrl: "/static/pictures/肖永庆.jpg"
  },
  {
    name: "申屠银洪",
    project: "桐君传统中药文化",
    tag: "古法中药传承者 | 国家级非遗传承人",
    desc: "传承桐君阁古法炮制技艺，建立非遗馆，培育多代中药传承人。",
    detailDesc: "申屠银洪深耕桐君传统中药文化数十年，坚守古法中药炮制工艺，对桐君阁经典方剂的配伍、炮制流程进行完整传承与保护。他建立了桐君中药非遗展示馆，通过口传心授的方式培养中青年传承人，让传统中药文化得以活态传承。",
    imgUrl: "/static/pictures/申屠银洪.jpg"
  },
  {
    name: "王俊良",
    project: "人参炮制技艺",
    tag: "人参古法炮制专家 | 第五批国家级非遗传承人",
    desc: "专注人参传统炮制工艺，保留人参药效活性，推动道地人参产业化。",
    detailDesc: "王俊良精通人参的洗、晒、蒸、制等古法炮制工序，深谙不同炮制方法对人参药效的影响，所炮制的人参饮片药效稳定、品质上乘。他在传承古法的同时，结合现代仓储技术，解决了道地人参的保存难题，推动人参炮制技艺与产业发展深度融合。",
    imgUrl: "/static/pictures/王俊良.jpg"
  }
]);

// 显示传承人详情弹窗
const showInheritorDetail = (inheritor) => {
  currentInheritor.value = inheritor;
  showModal.value = true;
  // 禁止页面滚动（弹窗显示时）
  document.body.style.overflow = "hidden";
};

// 关闭传承人详情弹窗
const closeModal = () => {
  showModal.value = false;
  currentInheritor.value = {};
  // 恢复页面滚动
  document.body.style.overflow = "auto";
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
  flex-wrap: nowrap; /* 强制不换行 */
  min-width: 0; /* 允许 flex item 缩小 */
  overflow-x: auto; /* 如果实在太窄，允许横向滚动而不是换行 */
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}
.nav-center::-webkit-scrollbar {
  display: none;
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
  white-space: nowrap; /* 文字不换行 */
  flex-shrink: 0; /* 防止被压缩 */
}

.nav-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  flex-shrink: 0; /* 图标不压缩 */
}

.nav-icon {
  font-size: 20px;
  transition: transform 0.3s ease;
}

.nav-label {
  transition: color 0.3s ease;
  white-space: nowrap; /* 再次确保标签文字不换行 */
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

.user-entry {
  position: relative;
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(255, 255, 255, 0.9);
  padding: 10px 14px;
  border-radius: 14px;
  box-shadow: 0 6px 20px rgba(111, 191, 154, 0.2);
  cursor: pointer;
  border: 1px solid rgba(111, 191, 154, 0.25);
  transition: all 0.3s ease;
}

.user-entry:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 26px rgba(111, 191, 154, 0.28);
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  letter-spacing: 1px;
}

.user-meta {
  display: flex;
  flex-direction: column;
  line-height: 1.2;
}

.user-name {
  font-weight: 700;
  color: var(--ink-green);
}

.user-phone {
  font-size: 12px;
  color: var(--sage-green);
  opacity: 0.8;
}

.user-arrow {
  color: var(--sage-green);
  font-size: 18px;
}

.user-menu {
  position: absolute;
  right: 0;
  top: 60px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.05);
  padding: 8px;
  min-width: 160px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  z-index: 2000;
}

.menu-action {
  padding: 10px 12px;
  background: #f8fdfa;
  border: 1px solid rgba(111, 191, 154, 0.2);
  border-radius: 10px;
  color: var(--ink-green);
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
}

.menu-action:hover {
  background: rgba(111, 191, 154, 0.12);
  border-color: var(--primary);
}

.menu-action.danger {
  color: #c03434;
  border-color: rgba(192, 52, 52, 0.18);
  background: #fff7f7;
}

.menu-action.danger:hover {
  background: #ffeaea;
  border-color: #c03434;
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

  /* 移动端进一步减少背景草 */+                                                                                                                    ·
  .background-herbs-layer .background-herb:nth-child(n+16) {
    display: none;
  }

  .background-herb {
    opacity: 0.02 !important;
  }

}
/* ====== 5. 道地药材产地分布模块样式 ====== */
.herb-distribution-section {
  width: 100%;
  min-height: 700px;
  position: relative;
  z-index: 20;
  padding: 80px 8% 120px;
  background: rgba(247, 249, 244, 0.85);
  backdrop-filter: blur(8px);
  margin-top: 40px;
}

.distribution-title-wrapper {
  text-align: center;
  margin-bottom: 40px;
}

.distribution-main-title {
  font-size: 2.8rem;
  font-weight: 900;
  color: var(--ink-green);
  margin: 0 0 12px 0;
  font-family: 'ZCOOL XiaoWei', serif;
  letter-spacing: 3px;
}

.distribution-subtitle {
  font-size: 16px;
  color: var(--sage-green);
  margin: 0 0 16px 0;
  letter-spacing: 2px;
}

.title-divider {
  width: 80px;
  height: 2px;
  background: linear-gradient(90deg, var(--gold-accent), transparent);
  margin: 0 auto;
}

/* 地图容器 */
.map-container {
  width: 100%;
  height: 500px;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 15px 40px rgba(26, 61, 46, 0.15), 0 5px 15px rgba(26, 61, 46, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.8);
  position: relative;
}

/* 筛选面板 */
.herb-filter-panel {
  position: absolute;
  top: 20px;
  left: 20px;
  z-index: 100;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(12px);
  padding: 16px 20px;
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(26, 61, 46, 0.1);
  border: 1px solid rgba(45, 90, 71, 0.1);
  max-width: 320px;
}

.filter-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  font-weight: 700;
  color: var(--ink-green);
  font-size: 15px;
}

.filter-title i {
  color: var(--gold-accent);
  font-size: 18px;
}

.filter-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 10px;
}

.filter-tag {
  padding: 6px 12px;
  background: rgba(45, 90, 71, 0.08);
  border: 1px solid rgba(45, 90, 71, 0.15);
  border-radius: 20px;
  font-size: 13px;
  color: var(--sage-green);
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-tag.active {
  /* 绿色渐变背景（可根据你的主色调整色值） */
  background: linear-gradient(135deg, #2D5D46, #3E7D65);
  /* 文字用浅米色（非纯白），比纯白更贴合中式风格 */
  color: #F8F5F0;
  border-color: #2D5D46;
  box-shadow: 0 4px 12px rgba(45, 90, 71, 0.2);
  transform: translateY(-2px);
}
.filter-tag:hover:not(.active) {
  border-color: var(--gold-accent);
  transform: translateY(-2px);
}

.herb-tip {
  font-size: 12px;
  color: var(--sage-green);
  opacity: 0.7;
  display: flex;
  align-items: center;
  gap: 4px;
}

.herb-tip i {
  font-size: 12px;
}

/* 地图信息窗口样式 */
.herb-info-window {
  padding: 12px 16px;
  font-family: 'Noto Serif SC', serif;
  width: 220px;
}

.info-name {
  font-size: 18px;
  font-weight: 700;
  color: var(--ink-green);
  margin: 0 0 6px 0;
  border-bottom: 1px solid rgba(197, 166, 102, 0.3);
  padding-bottom: 4px;
}

.info-alias {
  font-size: 12px;
  color: var(--gold-accent);
  margin: 0 0 4px 0;
}

.info-efficacy {
  font-size: 13px;
  color: var(--sage-green);
  margin: 0 0 4px 0;
  line-height: 1.5;
}

.info-feature {
  font-size: 13px;
  color: #4a6659;
  margin: 0;
  line-height: 1.5;
}

/* 响应式适配 */
@media (max-width: 1200px) {
  .herb-distribution-section {
    padding: 60px 6% 100px;
  }
  .map-container {
    height: 450px;
  }
  .herb-filter-panel {
    max-width: 280px;
    padding: 12px 16px;
  }
}

@media (max-width: 768px) {
  .herb-distribution-section {
    padding: 40px 4% 80px;
    min-height: 500px;
  }
  .distribution-main-title {
    font-size: 2rem;
  }
  .map-container {
    height: 400px;
  }
  .herb-filter-panel {
    position: relative;
    top: 0;
    left: 0;
    max-width: 100%;
    margin: 0 auto 20px;
  }
  .herb-info-window {
    width: 180px;
  }
}
/* ====== 4. 中药非遗传承人展示模块样式 ====== */
.heritage-section {
  width: 100%;
  min-height: 600px;
  position: relative;
  z-index: 20;
  padding: 100px 8% 80px;
  background: rgba(247, 249, 244, 0.9);
  backdrop-filter: blur(8px);
  margin-top: 40px;
}

/* 标题样式 */
.heritage-title {
  text-align: center;
  margin-bottom: 50px;
}

.heritage-title h2 {
  font-size: 2.8rem;
  font-weight: 900;
  color: var(--ink-green);
  margin: 0 0 12px 0;
  font-family: 'ZCOOL XiaoWei', serif;
  letter-spacing: 3px;
}

.heritage-title p {
  font-size: 16px;
  color: var(--sage-green);
  margin: 0;
  letter-spacing: 2px;
  opacity: 0.8;
}

/* 卡片容器（响应式网格） */
.heritage-card-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
  justify-items: center;
}

/* 传承人卡片 */
.heritage-card {
  width: 100%;
  max-width: 320px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(12px);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(26, 61, 46, 0.12), 0 4px 15px rgba(26, 61, 46, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.9);
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.heritage-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 20px 40px rgba(26, 61, 46, 0.18), 0 8px 20px rgba(26, 61, 46, 0.12);
  border-color: var(--gold-accent);
}

/* 卡片图片 */
.card-img {
  width: 100%;
  height: 180px;
  object-fit: cover;
  display: block;
  transition: transform 0.6s ease;
}

.heritage-card:hover .card-img {
  transform: scale(1.08);
}

/* 卡片内容 */
.card-content {
  padding: 20px 16px;
}

.card-name {
  font-size: 18px;
  font-weight: 700;
  color: var(--ink-green);
  margin-bottom: 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.card-project {
  font-size: 13px;
  font-weight: 500;
  color: var(--gold-accent);
  opacity: 0.8;
  letter-spacing: 1px;
}

.card-tag {
  font-size: 12px;
  color: var(--sage-green);
  padding: 4px 8px;
  background: rgba(45, 90, 71, 0.08);
  border-radius: 8px;
  display: inline-block;
  margin-bottom: 12px;
}

.card-desc {
  font-size: 14px;
  color: #4a6659;
  line-height: 1.6;
  opacity: 0.9;
}

/* 详情弹窗 */
.detail-modal {
  position: fixed;
  inset: 0;
  background: rgba(26, 61, 46, 0.7);
  backdrop-filter: blur(8px);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.modal-content {
  width: 100%;
  max-width: 800px;
  background: #fff;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
  position: relative;
  display: grid;
  grid-template-columns: 1fr 1.5fr;
}

.modal-close {
  position: absolute;
  top: 16px;
  right: 16px;
  font-size: 24px;
  color: var(--sage-green);
  cursor: pointer;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.8);
  z-index: 10;
  transition: all 0.3s ease;
}

.modal-close:hover {
  background: var(--gold-accent);
  color: #fff;
  transform: rotate(90deg);
}

.modal-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.modal-info {
  padding: 30px 25px;
}

.modal-info h3 {
  font-size: 22px;
  font-weight: 900;
  color: var(--ink-green);
  margin: 0 0 12px 0;
  border-bottom: 2px solid rgba(197, 166, 102, 0.3);
  padding-bottom: 10px;
}

.modal-tag {
  font-size: 13px;
  color: var(--gold-accent);
  margin: 0 0 16px 0;
  letter-spacing: 1px;
}

.modal-desc {
  font-size: 15px;
  color: #4a6659;
  line-height: 1.8;
  margin: 0;
  text-align: justify;
}

/* 响应式适配 */
@media (max-width: 1200px) {
  .heritage-section {
    padding: 80px 6% 60px;
  }
  .modal-content {
    max-width: 650px;
  }
}

@media (max-width: 768px) {
  .heritage-section {
    padding: 60px 4% 40px;
    min-height: 500px;
  }
  .heritage-title h2 {
    font-size: 2rem;
  }
  .heritage-card-container {
    gap: 20px;
  }
  .modal-content {
    grid-template-columns: 1fr;
    max-width: 400px;
  }
  .modal-img {
    height: 200px;
  }
  .modal-info {
    padding: 20px 16px;
  }
  .modal-info h3 {
    font-size: 18px;
  }
}
/* 新增：操作按钮样式 */
/* 新增：操作按钮样式 */
.add-herb-btn {
  margin-top: 20px;
  padding: 12px 24px;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: #fff;
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(111, 191, 154, 0.3);
  /* 新增：调整位置，避免遮挡筛选面板 */
  position: absolute;
  top: 20px;
  right: 20px;
  z-index: 99;
}

.add-herb-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(111, 191, 154, 0.4);
}

/* 新增：药材表单弹窗样式 */
.herb-form-modal {
  position: fixed;
  inset: 0;
  background: rgba(26, 61, 46, 0.7);
  backdrop-filter: blur(8px);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.modal-inner {
  width: 100%;
  max-width: 600px;
  background: #fff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}

.modal-header {
  padding: 16px 20px;
  border-bottom: 1px solid rgba(45, 90, 71, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.modal-header h3 {
  margin: 0;
  color: var(--ink-green);
  font-weight: 700;
}

.modal-close {
  font-size: 24px;
  color: var(--sage-green);
  cursor: pointer;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.modal-close:hover {
  background: rgba(45, 90, 71, 0.08);
  color: var(--gold-accent);
}

.modal-form {
  padding: 20px;
}

.form-item {
  margin-bottom: 16px;
}

.form-item label {
  display: block;
  margin-bottom: 6px;
  color: var(--ink-green);
  font-weight: 500;
  font-size: 14px;
}

.form-item input,
.form-item select,
.form-item textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid rgba(45, 90, 71, 0.15);
  border-radius: 8px;
  font-family: 'Noto Serif SC', serif;
  color: var(--sage-green);
  background: rgba(247, 249, 244, 0.5);
  transition: border-color 0.3s ease;
}

.form-item input:focus,
.form-item select:focus,
.form-item textarea:focus {
  outline: none;
  border-color: var(--gold-accent);
  box-shadow: 0 0 0 2px rgba(197, 166, 102, 0.1);
}

.form-item textarea {
  min-height: 80px;
  resize: vertical;
}

.modal-footer {
  padding: 16px 20px;
  border-top: 1px solid rgba(45, 90, 71, 0.1);
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
}

.btn-cancel {
  padding: 8px 16px;
  background: rgba(45, 90, 71, 0.08);
  border: 1px solid rgba(45, 90, 71, 0.15);
  border-radius: 8px;
  color: var(--sage-green);
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-cancel:hover {
  background: rgba(45, 90, 71, 0.12);
}

.btn-confirm {
  padding: 8px 16px;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-confirm:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-confirm:hover:not(:disabled) {
  background: linear-gradient(135deg, var(--primary-dark), #1e4a3d);
}

/* 新增：删除确认弹窗样式 */
.delete-confirm-modal {
  position: fixed;
  inset: 0;
  background: rgba(26, 61, 46, 0.7);
  backdrop-filter: blur(8px);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.delete-modal-inner {
  width: 100%;
  max-width: 400px;
  background: #fff;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}

.delete-modal-inner h3 {
  margin: 0 0 12px 0;
  color: var(--ink-green);
  font-weight: 700;
  text-align: center;
}

.delete-modal-inner p {
  margin: 0 0 20px 0;
  color: #4a6659;
  text-align: center;
  line-height: 1.6;
}

.delete-btn-group {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.btn-delete {
  padding: 8px 16px;
  background: linear-gradient(135deg, #e53e3e, #c53030);
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-delete:hover {
  background: linear-gradient(135deg, #c53030, #a32020);
}

/* 窗口容器：留白+薄阴影+圆角 */
.herb-info-window-refined {
  width: 280px;
  padding: 16px 20px;
  background: #fff;
  border-radius: 10px;
  border: 1px solid #e6eee9;
  box-shadow: 0 4px 15px rgba(26, 61, 46, 0.08);
  font-family: 'Noto Serif SC', serif;
  position: relative;
}

/* 名称+印章区域：错落排版 */
.info-top {
  display: flex;
  align-items: baseline;
  gap: 8px;
  margin-bottom: 12px;
}

.info-name-refined {
  font-size: 20px;
  font-weight: 800;
  color: #1a3d2e;
  margin: 0;
  letter-spacing: 1px;
  font-family: 'ZCOOL XiaoWei', serif;
}

/* 道地印章：仿真篆刻效果 */
.seal-mark {
  font-size: 12px;
  color: #c5a666;
  border: 2px solid #c5a666;
  padding: 2px 6px;
  border-radius: 4px;
  font-weight: 700;
  letter-spacing: 2px;
  transform: rotate(-5deg);
  background: rgba(197, 166, 102, 0.05);
}

/* 生境分布：中式分隔线+文字层次 */
.info-habitat-refined {
  padding-top: 8px;
  border-top: 1px dashed #dcece6;
  margin-bottom: 14px;
  line-height: 1.8;
}

.habitat-label {
  display: block;
  font-size: 13px;
  color: #2d5a47;
  font-weight: 600;
  margin-bottom: 4px;
}

.habitat-value {
  font-size: 14px;
  color: #4a6659;
  word-break: break-all;
}

/* 操作按钮：悬浮水墨按钮 */
/* 操作按钮容器：调整间距 */
.info-ops-refined {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
  margin-top: 8px;
}

/* 编辑按钮：墨绿+印章纹理 */
.btn-edit-refined {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 5px 10px;
  border-radius: 6px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #2d5a47;
  background: linear-gradient(120deg, rgba(45, 90, 71, 0.05), rgba(45, 90, 71, 0.1));
  color: #2d5a47;
  font-family: 'Noto Serif SC', serif;
}
.btn-edit-refined i {
  font-size: 14px;
}
.btn-edit-refined:hover {
  background: linear-gradient(120deg, #2d5a47, #1a3d2e);
  color: #fff;
  box-shadow: 0 2px 8px rgba(45, 90, 71, 0.2);
  transform: translateY(-1px);
}

/* 删除按钮：琥珀+宣纸纹理 */
.btn-del-refined {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 5px 10px;
  border-radius: 6px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #c5a666;
  background: linear-gradient(120deg, rgba(197, 166, 102, 0.05), rgba(197, 166, 102, 0.1));
  color: #c5a666;
  font-family: 'Noto Serif SC', serif;
}
.btn-del-refined i {
  font-size: 14px;
}
.btn-del-refined:hover {
  background: linear-gradient(120deg, #c5a666, #a38450);
  color: #fff;
  box-shadow: 0 2px 8px rgba(197, 166, 102, 0.2);
  transform: translateY(-1px);
}
</style>
