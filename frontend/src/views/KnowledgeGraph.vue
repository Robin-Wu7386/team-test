<template>
  <div class="knowledge-graph-page">
    <!-- 头部 - 完全对应原代码 -->
    <header>
      <div class="logo">中医药知识图谱推演</div>
      <button @click="goToHome" class="back-button">返回主页</button>
    </header>

    <!-- 主容器 - 完全对应原代码 -->
    <div class="main-container">
      <!-- 左侧查询面板 - 完全对应原代码 -->
      <div class="query-panel">
        <div>
          <h2>中药材 / 方剂查询</h2>
          <div class="search-box">
            <input
              type="text"
              id="searchInput"
              v-model="searchInput"
              placeholder="输入药材或方剂名称，如'黄芪'"
              @keypress="handleKeyPress"
              @input="handleInput"
            >
            <button class="search-button" @click="performSearch">查询</button>
          </div>
        </div>
        <div>
          <h3>最近查询</h3>
          <div class="history-list">
            <div
              v-for="(item, index) in historyItems"
              :key="index"
              class="history-item"
              :id="'history-item-' + (index + 1)"
              @click="loadHistory(item)"
              :style="getHistoryItemStyle(item)"
            >
              {{ item || '暂无历史' }}
            </div>
          </div>
        </div>
        <div class="result-info">
          <h4>查询结果</h4>
          <p id="resultText" v-html="resultText"></p>
        </div>
      </div>

      <!-- 右侧图谱区域 - 完全对应原代码 -->
      <div class="graph-panel">
        <div class="graph-header">
          <h2>知识图谱交互区</h2>
          <div class="graph-tools">
            <label style="margin-right: 10px; font-size: 14px; color: #555;">
              最大关联节点数：
              <input
                type="number"
                id="maxNodes"
                v-model.number="maxNodes"
                min="1"
                style="width: 60px; padding: 6px; border-radius: 6px; border: 2px solid var(--border);"
              >
            </label>
            <button @click="resetGraph">重置图谱</button>
          </div>
        </div>
        <div class="graph-container" id="graphContainer" ref="graphContainer">
          <!-- 知识图谱通过GraphVisualization组件动态生成 -->
          <GraphVisualization
            ref="graphVisualization"
            :nodes="graphData.nodes"
            :links="graphData.links"
            @node-click="handleNodeClick"
          />
        </div>
        <div class="footer-note">
          提示：拖拽节点可重新布局，点击节点可查看详情，鼠标滚轮可缩放视图。
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import GraphVisualization from '@/components/GraphVisualization.vue'
import { useHistoryStore } from '@/stores/history'
import { useNeo4jStore } from '@/stores/neo4j'
import { HERB_DISPLAY_ORDER, FANGJI_DISPLAY_ORDER, FANGJI_PROP_MAP } from '@/utils/constants'

const router = useRouter()
const historyStore = useHistoryStore()
const neo4jStore = useNeo4jStore()

// 数据状态 - 对应原代码变量
const searchInput = ref('')
const resultText = ref('在此显示药材或方剂的详细信息，包括性味、归经、功效、组成等。<br><br>请在上方搜索框中输入药材或方剂名称开始查询。')
const maxNodes = ref(20)
const historyItems = ref([null, null, null])
const graphData = ref({ nodes: [], links: [] })
const suggestionBox = ref(null)

// 返回首页函数
const goToHome = () => {
  // 方式1：使用Vue Router跳转（推荐，需提前配置首页路由）
  // router.push('/'); // 替换为你的首页路由路径，如 '/home'

  // 方式2：跳转到指定URL（适合无路由场景）
  window.location.href = '/'; // 替换为你的首页实际URL，如 'index.html'

  // 方式3：仅提示（测试用）
  // alert('返回首页');
};

// 挂载时初始化
onMounted(() => {
  // 连接数据库
  neo4jStore.initializeConnection()

  // 加载历史记录
  historyStore.loadHistory()
  historyItems.value = historyStore.historyItems

  console.log('Neo4j 连接成功')
})

// 卸载前清理
onBeforeUnmount(() => {
  neo4jStore.disconnect()
})

// 处理输入事件 - 对应原代码showSuggestions
const handleInput = async () => {
  const keyword = searchInput.value.trim()
  if (keyword.length < 2) {
    if (suggestionBox.value) {
      suggestionBox.value.innerHTML = ''
    }
    return
  }

  // 显示搜索建议
  await showSuggestions(keyword)
}

// 显示搜索建议 - 对应原代码showSuggestions函数
const showSuggestions = async (keyword) => {
  try {
    const suggestions = await neo4jStore.getSuggestions(keyword)
    createOrUpdateSuggestionBox(suggestions)
  } catch (error) {
    console.error('获取建议失败:', error)
  }
}

// 创建或更新建议框 - 对应原代码createSuggestionBox和相关逻辑
const createOrUpdateSuggestionBox = (suggestions) => {
  const input = document.getElementById('searchInput')
  if (!input) return

  if (!suggestionBox.value) {
    suggestionBox.value = document.createElement('div')
    suggestionBox.value.style.cssText = `
      position: absolute;
      top: 100%;
      left: 0;
      right: 0;
      background: white;
      border: 1px solid var(--border);
      border-top: none;
      border-radius: 0 0 12px 12px;
      max-height: 200px;
      overflow-y: auto;
      z-index: 100;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    `
    input.parentElement.style.position = 'relative'
    input.parentElement.appendChild(suggestionBox.value)
  }

  if (suggestions.length === 0) {
    suggestionBox.value.innerHTML = '<div style="padding:10px; color:#999;">无匹配结果</div>'
    return
  }

  suggestionBox.value.innerHTML = ''
  suggestions.forEach(suggestion => {
    const name = suggestion.name
    const labels = suggestion.labels
    const prefix = labels.includes('Fangji') ? '[方剂] ' : '[中药] '
    const item = document.createElement('div')
    item.textContent = prefix + name
    item.style.cssText = `
      padding: 12px 18px;
      cursor: pointer;
      border-bottom: 1px solid #eee;
    `
    item.onmouseover = () => item.style.background = '#f0f9f5'
    item.onmouseout = () => item.style.background = 'white'
    item.onclick = () => {
      searchInput.value = name
      if (suggestionBox.value) {
        suggestionBox.value.innerHTML = ''
      }
      queryExact(name)
    }
    suggestionBox.value.appendChild(item)
  })
}

// 处理回车键 - 对应原代码handleKeyPress
const handleKeyPress = (event) => {
  if (event.key === 'Enter') {
    performSearch()
  }
}

// 执行搜索 - 对应原代码performSearch
const performSearch = () => {
  const keyword = searchInput.value.trim()
  if (keyword) {
    queryExact(keyword)
  }
}

// 加载历史记录 - 对应原代码loadHistory
const loadHistory = (name) => {
  if (!name) return
  searchInput.value = name
  queryExact(name)
}

// 获取历史项样式 - 对应原代码中动态设置的样式
const getHistoryItemStyle = (item) => {
  if (item) {
    return {
      background: '#f9fdfa',
      cursor: 'pointer'
    }
  } else {
    return {
      background: '#f5f5f5',
      cursor: 'default'
    }
  }
}

// 精确查询 - 对应原代码queryExact函数
const queryExact = async (name) => {
  try {
    const result = await neo4jStore.performSearch(name)
    if (!result) {
      resultText.value = `未找到：${name}`
      clearGraph()
      return
    }

    if (result.type === 'herb') {
      renderHerbDetail(result.name, result.data)
    } else {
      renderFangjiDetail(result.name, result.data)
    }

    // 添加历史记录
    historyStore.addToHistory(name)
    historyItems.value = historyStore.historyItems

    // 渲染图谱
    await renderGraph(name, result.type)
  } catch (error) {
    console.error('查询错误:', error)
    resultText.value = '连接失败：' + error.message
  }
}

// 渲染中药详情 - 对应原代码renderHerbDetail函数
const renderHerbDetail = (name, attributesList) => {
  let html = `<strong style="font-size: 24px; color: var(--green);">${name}</strong><br><br>`

  if (!attributesList || attributesList.length === 0) {
    html += '暂无详细信息。'
    resultText.value = html
    return
  }

  attributesList.forEach((attr, index) => {
    if (!attr || !attr.properties) return

    const props = {}
    Object.keys(attr.properties).forEach(key => {
      const value = attr.properties[key]
      if (value && value !== 'NaN' && value !== '' && typeof value === 'string') {
        props[key] = value.trim()
      }
    })

    if (Object.keys(props).length === 0) return

    if (index > 0) {
      html += `<hr style="border: 0; border-top: 2px dashed #ddebe2; margin: 30px 0;"><br>`
    }

    let hasContent = false
    HERB_DISPLAY_ORDER.forEach(key => {
      if (key === '药材名称') return
      if (props[key]) {
        hasContent = true
        html += `<strong>${key}：</strong>${props[key].replace(/\n/g, '<br>')}<br><br>`
      }
    })

    Object.keys(props).forEach(key => {
      if (!HERB_DISPLAY_ORDER.includes(key)) {
        hasContent = true
        html += `<strong>${key}：</strong>${props[key].replace(/\n/g, '<br>')}<br><br>`
      }
    })

    if (!hasContent) {
      html += `<em style="color:#999;">（此来源无文本信息）</em><br><br>`
    }
  })

  resultText.value = html
}

// 渲染方剂详情 - 对应原代码renderFangjiDetail函数
const renderFangjiDetail = (name, propsObj) => {
  let html = `<strong style="font-size: 24px; color: var(--green);">${name}</strong><br><br>`

  const mapped = {}
  if (propsObj.prescription && propsObj.prescription !== 'NaN') mapped['处方'] = propsObj.prescription.trim()
  if (propsObj.preparation && propsObj.preparation !== 'NaN') mapped['制法'] = propsObj.preparation.trim()
  if (propsObj.function && propsObj.function !== 'NaN') mapped['功能主治'] = propsObj.function.trim()
  if (propsObj.usage && propsObj.usage !== 'NaN') mapped['用法用量'] = propsObj.usage.trim()
  if (propsObj.caution && propsObj.caution !== 'NaN') mapped['注意'] = propsObj.caution.trim()
  if (propsObj.excerpt && propsObj.excerpt !== 'NaN') mapped['摘录'] = propsObj.excerpt.trim()

  let hasContent = false
  FANGJI_DISPLAY_ORDER.forEach(key => {
    if (key === '方剂名称') return
    if (mapped[key]) {
      hasContent = true
      html += `<strong>${key}：</strong>${mapped[key].replace(/\n/g, '<br>')}<br><br>`
    }
  })

  if (!hasContent) {
    html += '暂无详细信息。'
  }

  resultText.value = html
}

// 渲染图谱 - 对应原代码renderGraph函数
const renderGraph = async (centerName, centerType) => {
  clearGraph()

  let limit = parseInt(maxNodes.value, 10)
  if (isNaN(limit) || limit < 1) {
    limit = 20
    maxNodes.value = 20
  }

  try {
    const data = await neo4jStore.getGraphData(centerName, centerType, limit)
    graphData.value = data
  } catch (error) {
    console.error('图谱错误:', error)
  }
}

// 清除图谱 - 对应原代码clearGraph函数
const clearGraph = () => {
  graphData.value = { nodes: [], links: [] }
}

// 重置图谱 - 对应原代码resetGraph函数
const resetGraph = () => {
  clearGraph()
  resultText.value = '在此显示药材或方剂的详细信息，包括性味、归经、功效、组成等。<br><br>请在上方搜索框中输入药材或方剂名称开始查询。'
}

// 处理节点点击 - 对应原代码中节点点击事件
const handleNodeClick = async (nodeId) => {
  await queryExact(nodeId)
}

// 返回主界面 - 对应原代码onclick事件
const goBack = () => {
  window.location.href = 'index.html'
}

// 监听maxNodes变化 - 对应原代码注释掉的监听器
watch(maxNodes, (newValue) => {
  const currentName = searchInput.value.trim()
  if (currentName && graphData.value.nodes.length > 0) {
    const isHerb = graphData.value.nodes.some(n => n.id === currentName && n.type === 'herb')
    renderGraph(currentName, isHerb ? 'herb' : 'fangji')
  }
})

// 点击外部关闭建议框 - 对应原代码document监听器
const handleDocumentClick = (event) => {
  if (suggestionBox.value && !event.target.closest('.search-box')) {
    suggestionBox.value.innerHTML = ''
  }
}

onMounted(() => {
  document.addEventListener('click', handleDocumentClick)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleDocumentClick)
  if (suggestionBox.value) {
    suggestionBox.value.remove()
  }
})
</script>

<style scoped>
/* 头部 - 完全复制原CSS */
header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px;
  height: 70px;
  background: var(--header-bg);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}
.logo {
  font-weight: 700;
  font-size: 22px;
  color: var(--yellow);
}
.back-button {
  padding: 10px 24px;
  font-size: 16px;
  border-radius: 20px;
  background: var(--green);
  border: none;
  color: white;
  cursor: pointer;
  transition: 0.3s;
}
.back-button:hover {
  background: #5daa87;
  transform: scale(1.05);
}

/* 主容器 - 完全复制原CSS */
.main-container {
  display: flex;
  height: calc(100vh - 70px);
  padding: 20px;
  gap: 20px;
}

/* 左侧查询面板 - 完全复制原CSS */
.query-panel {
  width: 33.33%;
  background: var(--card-bg);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.query-panel h2 {
  color: var(--green);
  font-size: 20px;
  margin-bottom: 10px;
  border-bottom: 2px solid var(--yellow);
  padding-bottom: 8px;
}
.search-box {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}
.search-box input {
  flex: 1;
  padding: 12px 18px;
  border: 1px solid var(--border);
  border-radius: 20px;
  font-family: "Noto Serif SC", serif;
  font-size: 15px;
  outline: none;
  transition: 0.3s;
}
.search-box input:focus {
  border-color: var(--green);
  box-shadow: 0 0 0 2px rgba(111, 191, 154, 0.2);
}
.search-button {
  padding: 12px 24px;
  border: none;
  border-radius: 20px;
  background: linear-gradient(135deg, var(--green), var(--yellow));
  color: white;
  font-weight: 500;
  cursor: pointer;
  transition: 0.3s;
}
.search-button:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}
.history-list {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: 10px;
}
.history-item {
  flex: 1;
  min-width: 80px;
  padding: 12px 16px;
  background: #f9fdfa;
  border-radius: 12px;
  border-left: 4px solid var(--green);
  cursor: pointer;
  transition: 0.3s;
  text-align: center;
  font-size: 14px;
}
.history-item:hover {
  background: #edf7f2;
  transform: translateY(-3px);
}
.result-info {
  background: #f9fdfa;
  border-radius: 12px;
  padding: 18px;
  border: 1px solid var(--border);
  flex: 1;
  min-height: 300px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}
.result-info h4 {
  color: var(--green);
  margin-bottom: 15px;
  font-size: 18px;
}
#resultText {
  font-size: 15px;
  line-height: 1.7;
  color: #555;
  flex: 1;
  margin: 0;
}

/* 右侧图谱区域 - 完全复制原CSS */
.graph-panel {
  flex: 1;
  background: var(--card-bg);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.graph-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.graph-header h2 {
  color: var(--green);
  font-size: 20px;
}
.graph-tools button {
  padding: 8px 16px;
  margin-left: 10px;
  border: 2px solid var(--border);
  border-radius: 20px;
  background: white;
  cursor: pointer;
  transition: 0.3s;
}
.graph-tools button:hover {
  background: var(--green);
  color: white;
}
.graph-container {
  flex: 1;
  background: #f9fdfa;
  border-radius: 12px;
  border: 1px dashed var(--border);
  position: relative;
  overflow: hidden;
}
.graph-container svg {
  width: 100%;
  height: 100%;
  display: block;
}
.footer-note {
  text-align: center;
  padding: 15px;
  font-size: 14px;
  color: #777;
  border-top: 1px solid var(--border);
  margin-top: 20px;
}

/* D3相关样式 - 完全复制原CSS */
.link {
  stroke: #6fbf9a;
  stroke-opacity: 0.6;
  pointer-events: none;
}
.link:hover {
  stroke-opacity: 1;
}
.node ellipse {
  transition: all 0.3s ease;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
}
.node ellipse:hover {
  transform: scale(1.1);
  filter: drop-shadow(0 4px 8px rgba(0,0,0,0.15));
}
.node text {
  pointer-events: none;
  user-select: none;
}
</style>
