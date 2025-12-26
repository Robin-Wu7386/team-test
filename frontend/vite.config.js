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
      // 新增：后端/api接口的代理配置（对应登录/注册接口）
      "/api": {
        target: "http://localhost:3001", // 后端服务地址
        changeOrigin: true, // 解决跨域
        rewrite: (path) => path.replace(/^\/api/, "") // 去掉请求路径中的/api前缀
      },
      // 保留原有的/chat和/static代理
      "/chat": "http://127.0.0.1:8000",
      "/static": "http://127.0.0.1:8000"
    }
  }
})