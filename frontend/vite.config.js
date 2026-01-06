import { defineConfig } from "vite"
import vue from "@vitejs/plugin-vue"
import { fileURLToPath, URL } from "node:url"

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url))
    }
  },
  server: {
    proxy: {
        // 用户后端API（登录/注册等）- 端口3001
      "/api/user": {
        target: "http://localhost:3001",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/user/, "")
      },
      // 管理员后端API - 端口8000
      "/api/admin": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
      // 保留原有的/chat和/static代理
      "/chat": "http://127.0.0.1:8000",
      "/static": "http://127.0.0.1:8000"
    }
  }
})