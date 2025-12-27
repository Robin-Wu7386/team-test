import { createRouter, createWebHistory } from "vue-router";
import Home from "./views/Home.vue";
import AIChat from "./views/AIChat.vue";
import AIConsultWizard from "./views/AIConsultWizard.vue";
import KnowledgeGraph from "./views/KnowledgeGraph.vue"; // 新增导入
import Login from './views/Login.vue';
import Register from './views/Register.vue';
import HerbRecommend from '../views/HerbRecommend.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", component: Home },
    { path: "/chat_page", component: AIChat },
    { path: "/ai_consult_wizard", component: AIConsultWizard },
    { path: "/knowledge_graph", component: KnowledgeGraph }, // 新增路由
    { path: '/login', component: Login }, // 登录页路由
    { path: '/register', component: Register }// 注册页路由
      {
    path: '/herb-recommend',
    name: 'HerbRecommend',
    component: HerbRecommend
  },
  {
  ]
});
