import { createApp } from "vue";
import { createPinia } from "pinia";
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/js/bootstrap.bundle.js';
import App from "./App.vue";
import router from "./router";

const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);
const app = createApp(App);

// app.use(createPinia());
app.use(pinia);
app.use(router);

app.mount("#app");
