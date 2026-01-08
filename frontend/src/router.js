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
  // 路由规则数组（优化格式，补充缺失的name，统一引号风格）
  routes: [
    {
      path: "/",
      name: "Home", // 补充name，方便通过名称跳转（如router.push({name: 'Home'})）
      component: Home
    }, // 首页
    {
      path: "/chat_page",
      name: "AIChat", // 补充name
      component: AIChat
    }, // AI问诊聊天页
    {
      path: "/knowledge_graph",
      name: "KnowledgeGraph", // 补充name
      component: KnowledgeGraph
    }, // 知识图谱页
    {
      path: "/comments",
      name: "Comments", // 补充name
      component: Comments
    }, // 评论区
    {
      path: "/profile",
      name: "Profile", // 补充name
      component: Profile
    }, // 个人中心
    {
      path: '/login',
      name: "Login", // 补充name
      component: Login,
      meta: { hideNav: true }
    }, // 登录页
    {
      path: '/register',
      name: "Register", // 补充name
      component: Register,
      meta: { hideNav: true }
    }, // 注册页
    {
      path: '/admin/login',
      name: "AdminLogin", // 补充name
      component: AdminLogin,
      meta: { hideNav: true }
    },
    {
      path: '/admin/backend',
      name: "AdminBackend", // 补充name
      component: AdminBackend,
      meta: { requiresAuth: true } // 需要管理员登录验证
    },
    {
      path: '/recommend',
      name: 'HerbRecommend',
      component: HerbRecommend
    },
    {
      path: '/admin/users',
      name: 'AdminUsers',
      component: AdminUsers
    }
  ],
  // 新增：路由跳转后滚动到顶部（优化用户体验）
  scrollBehavior() {
    return { top: 0 };
  }
});