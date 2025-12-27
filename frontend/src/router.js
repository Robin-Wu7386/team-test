import { createRouter, createWebHistory } from "vue-router";
import Home from "./views/Home.vue";
import AIChat from "./views/AIChat.vue";
import AIConsultWizard from "./views/AIConsultWizard.vue";
import KnowledgeGraph from "./views/KnowledgeGraph.vue";
import Recommend from "./views/Recommend.vue";// 新增导入

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", component: Home },
    { path: "/chat_page", component: AIChat },
    { path: "/ai_consult_wizard", component: AIConsultWizard },
    { path: "/knowledge_graph", component: KnowledgeGraph },
    { path:"/recommend", component:Recommend }// 新增路由
  ]
});
