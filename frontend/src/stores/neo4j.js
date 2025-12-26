import { defineStore } from 'pinia'
import neo4jService from '@/services/neo4jService'

export const useNeo4jStore = defineStore('neo4j', {
  state: () => ({
    isConnected: false,
    currentSearch: '',
    searchResult: null,
    graphData: { nodes: [], links: [] }
  }),

  actions: {
    // 初始化连接
    async initializeConnection() {
      try {
        await neo4jService.connect()
        this.isConnected = true
        return true
      } catch (error) {
        console.error('连接失败:', error)
        this.isConnected = false
        return false
      }
    },

    // 断开连接
    disconnect() {
      neo4jService.disconnect()
      this.isConnected = false
    },

    // 执行搜索
    async performSearch(keyword) {
      this.currentSearch = keyword
      try {
        const result = await neo4jService.queryExact(keyword)
        this.searchResult = result
        return result
      } catch (error) {
        console.error('搜索失败:', error)
        this.searchResult = null
        throw error
      }
    },

    // 获取图谱数据
    async getGraphData(centerName, centerType, limit = 20) {
      try {
        const data = await neo4jService.getGraphData(centerName, centerType, limit)
        this.graphData = data
        return data
      } catch (error) {
        console.error('获取图谱数据失败:', error)
        throw error
      }
    },

    // 获取搜索建议
    async getSuggestions(keyword) {
      return await neo4jService.getSuggestions(keyword)
    },

    // 清空图谱
    clearGraph() {
      this.graphData = { nodes: [], links: [] }
    }
  }
})