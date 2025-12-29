import { HISTORY_KEY } from '@/utils/constants'

const historyService = {
  // 从 localStorage 加载历史记录
  loadHistoryFromStorage() {
    try {
      const stored = localStorage.getItem(HISTORY_KEY)
      return stored ? JSON.parse(stored) : []
    } catch (e) {
      console.error('读取历史记录失败:', e)
      return []
    }
  },

  // 保存历史记录到 localStorage
  saveHistoryToStorage(historyArray) {
    try {
      localStorage.setItem(HISTORY_KEY, JSON.stringify(historyArray))
    } catch (e) {
      console.error('保存历史记录失败:', e)
    }
  },

  // 添加新的查询到历史记录
  addToHistory(name) {
    let history = this.loadHistoryFromStorage()

    // 移除重复项
    history = history.filter(item => item !== name)

    // 添加到开头（最新）
    history.unshift(name)

    // 只保留最近3条
    history = history.slice(0, 3)

    this.saveHistoryToStorage(history)
    return history
  },

  // 获取格式化历史记录（确保总是3项）
  getFormattedHistory() {
    const history = this.loadHistoryFromStorage()
    // 创建历史项数组（按顺序：最新 -> 最旧）
    return [
      history[0] || null,  // 最新（最近一次）
      history[1] || null,  // 倒数第二次
      history[2] || null   // 倒数第三次
    ]
  }
}

export default historyService