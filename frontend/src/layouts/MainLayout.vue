<script setup>
import {ref, computed} from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useNavigatingStore } from '@/stores/useNavigatingStore';
import Toast from 'primevue/toast';

import QRCode from '@/assets/QR.jpg';

import Button from 'primevue/button';
import Breadcrumb from 'primevue/breadcrumb';
import ProgressSpinner from 'primevue/progressspinner';
import Dialog from 'primevue/dialog';

const navigatingStore = useNavigatingStore()
const router = useRouter()
const route = useRoute()


function goTo(path) {
  router.push({ name: path})
}
function toRickRoll() {
  window.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ', '_blank');
}
function openGitHub() {
  window.open('https://github.com/edgarsgogolevs/basketbols-ar-kaju', '_blank');
}

const visible = ref(false);

function showDialog() {
  visible.value = true;
}

const currentTab = computed(() => {
  return route.path
})

</script>
<template>
    <div class="main-layout">
      <div class="global-loader" v-if="navigatingStore.isNavigating ">
        <ProgressSpinner strokeWidth="6" animationDuration="1.5s" />
      </div>
      <header>
        <div class="ba-main-nav-button" :class="{ 'selected': currentTab === '/'}" @click="goTo('home')">
          <i class="mdi mdi-basketball mdi-36px" ></i>
            <h2>Basketbols ar kaju</h2>
        </div>
        <div class="ba-nav-menu">
          <div class="ba-nav-menu-button" :class="{ 'selected': currentTab === '/sandbox'}" @click="goTo('sandbox')">
            <i class="mdi mdi-test-tube mdi-36px sandbox"></i>
            <p class="ba-data">General</p>
          </div>
            <div class="ba-nav-menu-button" :class="{ 'selected': currentTab === '/models' || currentTab.startsWith('/model') }"  @click="goTo('models')">
            <i class="mdi mdi-brain mdi-36px models"></i>
            <p class="ba-data">AI Models</p>
          </div>
          <div class="ba-nav-menu-button" :class="{ 'selected': currentTab === '/games' || currentTab.startsWith('/game') }" @click="goTo('games')">
            <i class="mdi mdi-history mdi-36px history" ></i>
            <p class="ba-data">Games</p>
          </div>
          <div class="ba-nav-menu-button about" :class="{ 'selected': currentTab === '/teams'}" @click="goTo('teams')">
            <i class="mdi mdi-account-group-outline mdi-36px" ></i>
            <p class="ba-data">Teams</p>
          </div>
        </div>
        <div class="ba-main-small-nav-button" @click="showDialog">
            <i class="mdi mdi-information-outline mdi-36px" ></i>
        </div>

      </header>
      <main class="ba-main">
        
        <div v-if="route.path === '/'" class="ba-main-cover">
          <div class="ba-cover-form">
          <i class="mdi mdi-basketball main-logo" ></i>
          <div class="ba-cover-text">
            <h1>Basketbols ar kaju</h1>
            <p class="ba-description">AI predictions platform for National Basketball Association (NBA) basketball league</p>
          </div>

          <div class="ba-cover-buttons">
          <Button label="I need some predictions" @click="goTo('sandbox')" />
          <Button label="I'm rebellious AI" severity="secondary" @click="toRickRoll"/>
          </div>
        </div>
        </div>
        <Toast />
        <Dialog v-model:visible="visible" modal header="Header" :style="{ width: '50rem' }" :breakpoints="{ '1199px': '75vw', '575px': '90vw' }">
             <div class="qr-code">
              <img alt="code" :src="QRCode" class="dialog-image" />
              <div class="dialog-text">
                <h3 class="banana">Banana</h3>
                <p class="ba-description">This is a small project developed by RTU students as a study year project. It is a web application that uses machine learning models to predict the outcome of NBA games. The application is built using Vue.js and PrimeVue. The models are trained using Python and Scikit-learn. The data is collected using the NBA API. The source code is available on GitHub.</p>
                <div class="ba-cover-buttons">
                  <Button label="GitHub" @click="openGitHub"/>
                </div>  
              </div> 
             </div>
        </Dialog>
        <router-view />
      </main>
    </div>
  </template>
