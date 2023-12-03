import { createApp } from 'vue'
import { createPinia } from 'pinia';
import App from './App.vue'
import router from '@/router'
import PrimeVue from 'primevue/config';
import  ToastService  from 'primevue/toastservice';

import events from './router/events';

import MainLayout from './layouts/MainLayout.vue';

// import primevue styles
import 'primevue/resources/themes/lara-dark-purple/theme.css';
import 'primevue/resources/primevue.min.css'; 
import 'primeicons/primeicons.css'

import './assets/variables.css'
import './assets/prime-overrides.css'
import './assets/media-styles.css'
import './assets/styles.css'

events(router);
const app = createApp(App);
app.use(createPinia());
app.component('MainLayout', MainLayout);

// register router
app.use(router);
app.use(PrimeVue);
app.use(ToastService);

// maount app
app.mount('#app');