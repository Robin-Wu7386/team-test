<template>
  <div class="graph-container" ref="graphContainer"></div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import * as d3 from 'd3'

const props = defineProps({
  nodes: {
    type: Array,
    default: () => []
  },
  links: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['node-click'])

const graphContainer = ref(null)
let svg = null
let g = null
let linkGroup = null
let nodeGroup = null
let simulation = null
let zoomBehavior = null
let linkElements = null
let nodeElements = null

// 本地副本，用于模拟修改
const localNodes = ref([])
const localLinks = ref([])

// 更新本地副本
watch(() => props.nodes, (newNodes) => {
  localNodes.value = JSON.parse(JSON.stringify(newNodes))
}, { immediate: true })

watch(() => props.links, (newLinks) => {
  localLinks.value = JSON.parse(JSON.stringify(newLinks))
}, { immediate: true })

// 初始化图谱
const initForceGraph = () => {
  if (!graphContainer.value) return
  clearGraph()

  const container = graphContainer.value
  const width = container.clientWidth
  const height = container.clientHeight

  // 创建SVG - 修复：添加样式确保显示
  svg = d3.select(container)
    .html('')
    .append('svg')
    .attr('width', '100%')
    .attr('height', '100%')
    .style('display', 'block') // 关键修复：确保SVG显示

  // 添加背景矩形捕获事件 - 修复：正确的指针事件设置
  svg.append('rect')
    .attr('width', width)
    .attr('height', height)
    .attr('fill', 'none')
    .attr('pointer-events', 'all')

  g = svg.append('g')

  // 缩放行为 - 修复：使用正确的缩放配置
  zoomBehavior = d3.zoom()
    .scaleExtent([0.1, 8])
    .on('zoom', (event) => {
      g.attr('transform', event.transform)
      // 根据缩放调整线条和边框宽度
      if (linkElements) {
        linkElements.attr('stroke-width', 2 / event.transform.k)
      }
      if (nodeElements) {
        nodeElements.selectAll('ellipse')
          .attr('stroke-width', (d) => {
            const baseWidth = 2
            // 确保边框可见
            return Math.max(baseWidth / event.transform.k, 0.5)
          })
      }
    })

  svg.call(zoomBehavior)

  // 创建组
  linkGroup = g.append('g').attr('class', 'links')
  nodeGroup = g.append('g').attr('class', 'nodes')

  // 创建力导向模拟 - 修复：使用本地副本
  simulation = d3.forceSimulation(localNodes.value)
    .force('link', d3.forceLink(localLinks.value)
      .id(d => d.id)
      .distance(200)
    )
    .force('charge', d3.forceManyBody().strength(-1000))
    .force('center', d3.forceCenter(width / 2, height / 2))
    .force('collision', d3.forceCollide().radius(120))

  // 创建连线 - 修复：保存引用
  linkElements = linkGroup.selectAll('line')
    .data(localLinks.value)
    .enter()
    .append('line')
    .attr('class', 'link')
    .attr('stroke', '#6fbf9a')
    .attr('stroke-width', 2)
    .attr('stroke-opacity', 0.6)
    .style('pointer-events', 'none')

  // 创建节点 - 修复：保存引用
  nodeElements = nodeGroup.selectAll('g')
    .data(localNodes.value)
    .enter()
    .append('g')
    .attr('class', 'node')
    .call(d3.drag()
      .on('start', dragStarted)
      .on('drag', dragged)
      .on('end', dragEnded))

  // 节点椭圆
  nodeElements.append('ellipse')
    .attr('rx', d => getNodeWidth(d) / 2)
    .attr('ry', 28)
    .attr('fill', d => getNodeColor(d.type))
    .attr('stroke', d => getNodeBorderColor(d.type))
    .attr('stroke-width', 2)
    .attr('opacity', 0.95)

  // 节点文字
  nodeElements.append('text')
    .text(d => d.id)
    .attr('text-anchor', 'middle')
    .attr('dy', '0.3em')
    .attr('fill', '#2e4a3c')
    .attr('font-size', '14px')
    .attr('font-family', '"Noto Serif SC", serif')
    .attr('pointer-events', 'none')

  // 点击节点事件 - 修复：确保事件传播正确
  nodeElements.on('click', function(event, d) {
    event.stopPropagation()

    // 移除所有高亮
    nodeElements.selectAll('ellipse')
      .attr('stroke', nd => getNodeBorderColor(nd.type))
      .attr('stroke-width', 2)

    // 高亮当前节点
    d3.select(this).select('ellipse')
      .attr('stroke', '#2e4a3c')
      .attr('stroke-width', 3)

    // 触发节点点击事件
    emit('node-click', d.id)
  })

  // SVG点击事件：清除高亮
  svg.on('click', function(event) {
    if (event.target === this || event.target.tagName === 'rect') {
      nodeElements.selectAll('ellipse')
        .attr('stroke', d => getNodeBorderColor(d.type))
        .attr('stroke-width', 2)
    }
  })

  // 模拟更新
  simulation.on('tick', () => {
    // 更新连线位置
    linkElements
      .attr('x1', d => {
        // 确保source有坐标
        if (typeof d.source === 'object' && d.source !== null) {
          return d.source.x
        } else {
          const sourceNode = localNodes.value.find(n => n.id === d.source)
          return sourceNode ? sourceNode.x : 0
        }
      })
      .attr('y1', d => {
        if (typeof d.source === 'object' && d.source !== null) {
          return d.source.y
        } else {
          const sourceNode = localNodes.value.find(n => n.id === d.source)
          return sourceNode ? sourceNode.y : 0
        }
      })
      .attr('x2', d => {
        if (typeof d.target === 'object' && d.target !== null) {
          return d.target.x
        } else {
          const targetNode = localNodes.value.find(n => n.id === d.target)
          return targetNode ? targetNode.x : 0
        }
      })
      .attr('y2', d => {
        if (typeof d.target === 'object' && d.target !== null) {
          return d.target.y
        } else {
          const targetNode = localNodes.value.find(n => n.id === d.target)
          return targetNode ? targetNode.y : 0
        }
      })

    // 更新节点位置
    nodeElements.attr('transform', d => `translate(${d.x || 0},${d.y || 0})`)
  })

  // 模拟结束后自动居中
  simulation.on('end', () => {
    zoomToFit(600)
  })

  // 初始居中
  setTimeout(() => {
    zoomToFit(0)
  }, 100)
}

// 自动居中
const zoomToFit = (duration = 750) => {
  if (!localNodes.value.length || !nodeGroup || !svg) return

  const bounds = nodeGroup.node().getBBox()
  const fullWidth = svg.node().clientWidth
  const fullHeight = svg.node().clientHeight

  const padding = 100
  const width = bounds.width + padding * 2
  const height = bounds.height + padding * 2

  if (width === 0 || height === 0) return

  const midX = bounds.x + bounds.width / 2
  const midY = bounds.y + bounds.height / 2

  const scale = 0.9 / Math.max(width / fullWidth, height / fullHeight)
  const minScale = 0.3
  const maxScale = 2
  const finalScale = Math.min(maxScale, Math.max(minScale, scale))

  const translateX = fullWidth / 2 - finalScale * midX
  const translateY = fullHeight / 2 - finalScale * midY

  const transform = d3.zoomIdentity.translate(translateX, translateY).scale(finalScale)

  svg.transition()
    .duration(duration)
    .call(zoomBehavior.transform, transform)
}

// 节点宽度计算
const getNodeWidth = (d) => {
  return Math.max(80, d.id.length * 12 + 30)
}

// 节点颜色
const getNodeColor = (type) => {
  return type === 'herb' ? '#f0f9f5' : '#fef8f0'
}

// 节点边框颜色
const getNodeBorderColor = (type) => {
  return type === 'herb' ? '#6fbf9a' : '#f3b05a'
}

// 拖拽事件处理
const dragStarted = (event, d) => {
  if (!event.active) simulation.alphaTarget(0.3).restart()
  d.fx = d.x
  d.fy = d.y
}

const dragged = (event, d) => {
  d.fx = event.x
  d.fy = event.y
}

const dragEnded = (event, d) => {
  if (!event.active) simulation.alphaTarget(0)
  d.fx = null
  d.fy = null
}

// 清除图谱
const clearGraph = () => {
  if (simulation) {
    simulation.stop()
    simulation = null
  }
  if (graphContainer.value) {
    d3.select(graphContainer.value).html('')
  }
  svg = null
  g = null
  linkGroup = null
  nodeGroup = null
  zoomBehavior = null
  linkElements = null
  nodeElements = null
}

// 重置图谱（对外暴露）
const resetGraph = () => {
  clearGraph()
}

// 监听数据变化
watch(() => [props.nodes, props.links], () => {
  if (props.nodes.length > 0) {
    nextTick(() => {
      initForceGraph()
    })
  } else {
    clearGraph()
  }
}, { deep: true })

// 窗口大小变化时重新初始化
const handleResize = () => {
  if (props.nodes.length > 0) {
    initForceGraph()
  }
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
  if (props.nodes.length > 0) {
    // 等待DOM更新完成
    nextTick(() => {
      setTimeout(() => {
        initForceGraph()
      }, 100)
    })
  }
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  clearGraph()
})

// 暴露方法给父组件
defineExpose({
  resetGraph,
  zoomToFit
})
</script>

<style scoped>
.graph-container {
  width: 100%;
  height: 100%;
  background: #f9fdfa;
  border-radius: 12px;
  border: 1px dashed #ddebe2;
  overflow: hidden;
}

/* 确保D3样式能够穿透 */
:deep(.link) {
  stroke: #6fbf9a;
  stroke-opacity: 0.6;
  pointer-events: none;
}

:deep(.link:hover) {
  stroke-opacity: 1;
}

:deep(.node ellipse) {
  transition: all 0.3s ease;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
  cursor: pointer;
}

:deep(.node ellipse:hover) {
  filter: drop-shadow(0 4px 8px rgba(0,0,0,0.15));
}

:deep(.node text) {
  pointer-events: none;
  user-select: none;
}
</style>