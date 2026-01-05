import { defineConfig } from "vite"
import vue from "@vitejs/plugin-vue"
import { fileURLToPath, URL } from "node:url"

export default defineConfig({
  // 配置Vue插件
  plugins: [vue()],
  // 路径解析配置
  resolve: {
    alias: {
      // 配置 @ 指向 src 目录，方便组件导入
      "@": fileURLToPath(new URL("./src", import.meta.url))
    }
  },
  // 开发服务器配置
  server: {
    // 接口代理配置
    proxy: {
      // 用户后端API（登录/注册等）- 端口3001
      "/api/user": {
        target: "http://localhost:3001",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/user/, "/user")
      }, // 关键修复：补充逗号，分隔多个代理配置项
      // 管理员后端API - 端口3000
      "/api/admin": {
        target: "http://localhost:3000",
        changeOrigin: true,
        rewrite: (path) => path // 保持原路径不修改
      },
      // 保留原有的/chat和/static代理
      "/chat": "http://127.0.0.1:8000",
      "/static": "http://127.0.0.1:8000"
    }
  }
})