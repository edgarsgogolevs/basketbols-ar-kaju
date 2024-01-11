<script setup>
import { ref, onMounted } from 'vue';

import Teams from '@/components/Teams.vue';

import modelsService from '@/services/modelsService';

import useErrors from '@/hooks/useErrors';

const errors = useErrors();


const teams = ref();

const loading = ref(false);

async function load() {
  loading.value = true;
  try {
    const response = await modelsService.getAllTeams();
    if (response.status >= 200 && response.status < 300) {
        teams.value = response.data;
    }
  } catch (error) {
    errors.pushNotification({ severity: 'error', summary: 'Unexepected error', detail: 'Probably your internet connection or our server lag', life: 30000 });
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
    load();
});

</script>
<template>
  <div class="ba-main-form">
    <div class="ba-sticky-header">
        <div></div>
      <h2>Teams</h2>
    </div>

    <div class="ba-section">
        <Teams :teams="teams" />
    </div>  
  </div>
</template>
  
