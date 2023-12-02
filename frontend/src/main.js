import { createApp } from 'vue'
import { createPinia } from 'pinia';
import App from './App.vue'
import router from '@/router'
import PrimeVue from 'primevue/config';

import events from './router/events';

import MainLayout from './layouts/MainLayout.vue';

// import primevue styles
import 'primevue/resources/themes/lara-dark-purple/theme.css';
import 'primevue/resources/primevue.min.css'; 
import 'primeicons/primeicons.css'

import './assets/styles.css'
import './assets/media-styles.css'

events(router);
const app = createApp(App);
app.use(createPinia());
app.component('MainLayout', MainLayout);

// register router
app.use(router);
app.use(PrimeVue);

// maount app
app.mount('#app');