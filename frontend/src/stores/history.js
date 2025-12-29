import { defineStore } from 'pinia'
import historyService from '@/services/historyService'

export const useHistoryStore = defineStore('history', {
  state: () => ({
    historyItems: [null, null, null] // 对应3个历史项
  }),

  actions: {
    // 加载历史记录
    loadHistory() {
      const formatted = historyService.getFormattedHistory()
      this.historyItems = formatted
    },

    // 添加历史记录
    addToHistory(name) {
      const updatedHistory = historyService.addToHistory(name)
      this.historyItems = [
        updatedHistory[0] || null,
        updatedHistory[1] || null,
        updatedHistory[2] || null
      ]
    },

    // 清除历史记录
    clearHistory() {
      historyService.saveHistoryToStorage([])
      this.historyItems = [null, null, null]
    }
  }
})