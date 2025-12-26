import { createRouter, createWebHistory } from "vue-router";
import Home from "./views/Home.vue";
import AIChat from "./views/AIChat.vue";
import AIConsultWizard from "./views/AIConsultWizard.vue";

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", component: Home },
    { path: "/chat_page", component: AIChat },
    { path: "/ai_consult_wizard", component: AIConsultWizard }
  ]
});
