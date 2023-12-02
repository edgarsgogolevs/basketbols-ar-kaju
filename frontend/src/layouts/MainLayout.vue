<script setup>
import {ref, computed} from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useNavigatingStore } from '@/stores/useNavigatingStore';

import Button from 'primevue/button';
import ProgressSpinner from 'primevue/progressspinner';
import Dialog from 'primevue/dialog';

const navigatingStore = useNavigatingStore()
const router = useRouter()
const route = useRoute()


function goTo(path) {
  router.push(path)
}
function toRickRoll() {
  window.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ', '_blank');
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
        <div class="ba-main-nav-button" :class="{ 'selected': currentTab === '/'}" @click="goTo('/')">
          <i class="mdi mdi-basketball mdi-36px" ></i>
            <h2>Basketbols ar kaju</h2>

        </div>
        <div class="ba-nav-menu">
          <div class="ba-nav-menu-button" :class="{ 'selected': currentTab === '/sandbox'}" @click="goTo('sandbox')">
            <i class="mdi mdi-test-tube mdi-36px"></i>
            <p class="ba-data">Sandbox</p>
          </div>
            <div class="ba-nav-menu-button"  @click="goTo('games')">
            <i class="mdi mdi-brain mdi-36px"></i>
            <p class="ba-data">AI Predictions</p>
          </div>
          <div class="ba-nav-menu-button" @click="goTo('sandbox')">
            <i class="mdi mdi-history mdi-36px" ></i>
            <p class="ba-data">History</p>
          </div>
          <div class="ba-nav-menu-button" @click="goTo('sandbox')">
            <i class="mdi mdi-account-group-outline mdi-36px" ></i>
            <p class="ba-data">About Us</p>
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
        <Dialog v-model:visible="visible" modal header="Header" :style="{ width: '50rem' }" :breakpoints="{ '1199px': '75vw', '575px': '90vw' }">
              <p>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                  Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
                    Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
              </p>
        </Dialog>
        <router-view />
      </main>
    </div>
  </template>