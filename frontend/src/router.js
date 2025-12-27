// 导入Vue Router核心方法
import { createRouter, createWebHistory } from "vue-router";

// 导入页面组件（注意：路径需与实际文件结构匹配！）
// 假设当前router.js在 frontend/ 目录下，views文件夹也在frontend/目录下
import Home from "./views/Home.vue";
import AIChat from "./views/AIChat.vue";
import AIConsultWizard from "./views/AIConsultWizard.vue";
import KnowledgeGraph from "./views/KnowledgeGraph.vue";
import Login from './views/Login.vue';
import Register from './views/Register.vue';
// 修正路径：从 ../views 改为 ./views（保持路径层级统一）
import HerbRecommend from './views/HerbRecommend.vue'

// 创建并导出路由实例
export default createRouter({
  // 使用HTML5 History模式（无#号路由）
  history: createWebHistory(),
  // 路由规则数组（修正语法错误，补充完整）
  routes: [
    { path: "/", component: Home }, // 首页
    { path: "/chat_page", component: AIChat }, // AI问诊聊天页
    { path: "/ai_consult_wizard", component: AIConsultWizard }, // AI流程问诊页
    { path: "/knowledge_graph", component: KnowledgeGraph }, // 知识图谱页
    { path: '/login', component: Login }, // 登录页
    { path: '/register', component: Register }, // 注册页
    { // 中药推荐页（补充完整，无语法错误）
      path: '/herb-recommend',
      name: 'HerbRecommend',
      component: HerbRecommend
    }
  ]
});