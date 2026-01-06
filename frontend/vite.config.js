import { defineConfig } from "vite"
import vue from "@vitejs/plugin-vue"
import { fileURLToPath, URL } from "node:url"

// 完整无语法错误的Vite配置
export default defineConfig({
  plugins: [vue()], // Vue插件配置
  resolve: {
    alias: {
      // 配置@别名指向src目录，方便组件导入
      "@": fileURLToPath(new URL("./src", import.meta.url))
    }
  },
  server: {
    proxy: {
      // 用户后端API（登录/注册等）- 端口3001
      "/api/user": {
        target: "http://localhost:3001",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/user/, "/user")
      }, // 关键：补充了这个逗号，解决语法报错
      // 管理员后端API - 端口3000
      "/api/admin": {
        target: "http://localhost:3000",
        changeOrigin: true,
        rewrite: (path) => path // 保持原路径不修改
      },
      // 保留原有的/chat和/static代理（指向8000端口）
      "/chat": "http://127.0.0.1:8000",
      "/static": "http://127.0.0.1:8000"
    }
  }
})
