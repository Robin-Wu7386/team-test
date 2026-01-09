import { defineConfig } from "vite"
import vue from "@vitejs/plugin-vue"
import { fileURLToPath, URL } from "node:url"
import path from 'path'
import copy from 'rollup-plugin-copy'
import fs from 'fs'

// 最终版：适配tuijian-end包含.py和JSON文件，且与frontend同级（修正路径+增强容错）
export default defineConfig(({ command }) => {
  // ========== 核心路径修正（匹配你的实际层级） ==========
  // 源路径：frontend的上级目录下的tuijian-end/complete_herb_data.json（和.py同级）
  const jsonSourcePath = path.resolve(__dirname, '../tuijian-end/complete_herb_data.json')
  // 目标路径：frontend/public/tuijian-end（Vite能访问的静态资源目录）
  const jsonDestDir = path.resolve(__dirname, 'public/tuijian-end')

  // 启动前校验源文件是否存在，提前给出明确提示
  if (command === 'serve') {
    if (!fs.existsSync(jsonSourcePath)) {
      console.error('\x1b[31m❌ 源JSON文件不存在！\x1b[0m')
      console.error(`   预期路径：${jsonSourcePath}`)
      console.error(`   请检查：1. tuijian-end文件夹是否与frontend同级 2. JSON文件名是否拼写正确`)
    } else {
      console.log('\x1b[32m✅ 检测到源JSON文件存在\x1b[0m：', jsonSourcePath)
    }

    // 确保目标目录存在（避免复制时因目录不存在报错）
    if (!fs.existsSync(jsonDestDir)) {
      fs.mkdirSync(jsonDestDir, { recursive: true })
      console.log('\x1b[36mℹ️ 已自动创建目标目录\x1b[0m：', jsonDestDir)
    }
  }

  return {
    plugins: [
      vue(),
      // 自动复制JSON文件到public/tuijian-end
      copy({
        targets: [
          {
            src: jsonSourcePath,
            dest: jsonDestDir,
            rename: 'complete_herb_data.json' // 强制保留文件名，避免异常
          }
        ],
        hook: command === 'build' ? 'buildStart' : 'serveStart',
        verbose: true,
        overwrite: true,
        onCopy: (results) => {
          results.forEach(res => {
            if (res.status === 'success') {
              console.log('\x1b[32m✅ JSON文件复制成功\x1b[0m：')
              console.log(`   源：${res.source}`)
              console.log(`   目标：${path.join(res.dest, res.rename)}`)
            } else {
              console.error('\x1b[31m❌ JSON文件复制失败\x1b[0m：', res.error)
            }
          })
        }
      })
    ],
    resolve: {
      alias: {
        "@": fileURLToPath(new URL("./src", import.meta.url))
      }
    },
    server: {
      proxy: {
        "/api/daily-recommend": { target: "http://localhost:8000", changeOrigin: true, rewrite: (p) => p },
        "/api/user": { target: "http://localhost:3001", changeOrigin: true, rewrite: (p) => p.replace(/^\/api\/user/, "/user") },
        "/api/admin": { target: "http://localhost:3000", changeOrigin: true, rewrite: (p) => p },
        "/chat": "http://127.0.0.1:8000",
        "/static": "http://127.0.0.1:8000"
      },
      fs: {
        allow: ['..'] // 允许访问上级目录
      },
      strictPort: false,
      port: 5173
    },
    build: {
      outDir: 'dist',
      assetsDir: 'assets',
      assetsInclude: [jsonSourcePath]
    }
  }
})