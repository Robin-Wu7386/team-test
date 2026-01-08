import { defineStore } from 'pinia'

const STORAGE_KEY = 'userInfo'

export const useUserStore = defineStore('user', {
  state: () => ({
    userInfo: (() => {
      try {
        const cached = localStorage.getItem(STORAGE_KEY)
        return cached ? JSON.parse(cached) : null
      } catch (e) {
        return null
      }
    })()
  }),
  getters: {
    isLoggedIn: (state) => !!state.userInfo && !!state.userInfo.id
  },
  actions: {
    setUser(payload) {
      this.userInfo = payload
      localStorage.setItem(STORAGE_KEY, JSON.stringify(payload))
    },
    logout() {
      this.userInfo = null
      localStorage.removeItem(STORAGE_KEY)
    }
  }
})
