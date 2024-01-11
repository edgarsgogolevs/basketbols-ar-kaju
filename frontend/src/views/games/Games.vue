<script setup>
import { ref, onMounted, watch } from 'vue';

import TabMenu from 'primevue/tabmenu';

import modelsService from '@/services/modelsService';
import Games from '@/components/Games.vue';
import Toast from 'primevue/toast';
import useErrors from '@/hooks/useErrors';
import { useToast } from 'primevue/usetoast';

const errors = useErrors();

const active = ref(1);

watch(() => active.value,
  (newValue) => {
    if (newValue === 0) {
      loadRecentGames();
    } else {
      loadUpcomingGames();
    }
  }
);

const loading = ref(false);
const games = ref();

async function loadUpcomingGames() {
  loading.value = true;
  try {
    const response = await modelsService.getUpcomingGames(100);
    if (response.status >= 200 && response.status < 300) {
        games.value = response.data;
    }
    console.log(games.value);
  } catch (error) {
    console.error(error);
    errors.pushNotification({ severity: 'error', summary: 'Unexepected error', detail: '111Probably your internet connection or our server lag', life: 30000 });
  } finally {
    loading.value = false;
  }
}
async function loadRecentGames() {
  loading.value = true;
  try {
    const response = await modelsService.getRecentGames(100);
    if (response.status >= 200 && response.status < 300) {
        games.value = response.data;
    }
  } catch (error) {
    console.error(error);
    errors.pushNotification({ severity: 'error', summary: 'Unexepected error', detail: '111Probably your internet connection or our server lag', life: 30000 });
  } finally {
    loading.value = false;
  }
}

const items = ref([
    { label: 'Recent games', icon: 'pi pi-arrow-left' },
    { label: 'Upcoming games', icon: 'pi pi-arrow-right' },
]);

onMounted(() => {
    loadRecentGames();
    loadUpcomingGames();
});

</script>
<template>
<div class="ba-main-form">
    <div class="ba-sticky-header">
        <div></div>
        <h2>Games</h2>
    </div>
    <TabMenu :model="items" v-model:activeIndex="active" />
    <div class="ba-section">
        <Games :games="games" :upcoming="active" />
    </div> 
  </div>
</template>