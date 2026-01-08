// 导入Vue Router核心方法
import { createRouter, createWebHistory } from "vue-router";

// 导入页面组件（注意：路径需与实际文件结构匹配！）
// 假设当前router.js在 frontend/ 目录下，views文件夹也在frontend/目录下
import Home from "./views/Home.vue";
import AIChat from "./views/AIChat.vue";
import KnowledgeGraph from "./views/KnowledgeGraph.vue";
import Login from './views/Login.vue';
import Register from './views/Register.vue';
import AdminBackend from './views/AdminBackend.vue';
import AdminLogin from './views/AdminLogin.vue';
import Comments from './views/Comments.vue';
import Profile from './views/Profile.vue';
import AdminUsers from './views/AdminUsers.vue'; // 引入刚才新建的文件


import HerbRecommend from './views/HerbRecommend.vue'

// 创建并导出路由实例
export default createRouter({
  // 使用HTML5 History模式（无#号路由）
  history: createWebHistory(),
  // 路由规则数组（修正语法错误，补充完整）
  routes: [
    { path: "/", component: Home }, // 首页
    { path: "/chat_page", component: AIChat }, // AI问诊聊天页
    { path: "/knowledge_graph", component: KnowledgeGraph }, // 知识图谱页
    { path: "/comments", component: Comments }, // 评论区
    { path: "/profile", component: Profile }, // 个人中心
    { path: '/login', component: Login, meta: { hideNav: true } }, // 登录页
    { path: '/register', component: Register, meta: { hideNav: true } }, // 注册页
    { path: '/admin/login', component: AdminLogin, meta: { hideNav: true } },
    {
      path: '/admin/backend',
      component: AdminBackend,
      meta: { requiresAuth: true } // 需要管理员登录验证
    },
    { // 中药推荐页（补充完整，无语法错误）
      path: '/recommend',
      name: 'HerbRecommend',
      component: HerbRecommend
    },
    {
  path: '/admin/users',
  name: 'AdminUsers',
  component: AdminUsers
}
  ]
});
