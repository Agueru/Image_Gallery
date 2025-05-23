import "./assets/main.css";
import "bootstrap/dist/css/bootstrap.css";
import 'vue3-toastify/dist/index.css';

import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";

const app = createApp(App);

app.use(router);
app.use(store)

app.mount("#app");
