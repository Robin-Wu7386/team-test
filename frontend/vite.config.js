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
      // 1. 【图片】转发给 Python (5000)
      "/static": {
        target: "http://localhost:5000",
        changeOrigin: true
      },

      // 2. 【管理员】转发给 Admin Node (3000)
      "/api/admin": {
        target: "http://localhost:3000",
        changeOrigin: true
      },

      // 3. 【评论】单独配置，确保转发给 User Node (3001)
      // 前端请求 /api/comments -> 转发给 http://localhost:3001/comments
      "/api/comments": {
        target: "http://localhost:3001",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, "")
      },

      // 4. 【用户登录/注册】单独配置
      // 前端请求 /api/user/... -> 转发给 http://localhost:3001/user/...
      "/api/user": {
        target: "http://localhost:3001",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, "")
      }
    }
  }
})