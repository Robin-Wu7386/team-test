import { createApp } from "vue";
import { createPinia } from "pinia"; // 新增这行
import App from "./App.vue";
import router from "./router";
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'


const app = createApp(App);
const pinia = createPinia(); // 新增这行

app.use(pinia); // 新增这行，必须在 router 前面
app.use(router);
app.mount("#app");