<script setup>
import { ref, onMounted } from 'vue';

import Card from '@/components/Card.vue';
import Column from 'primevue/column';
import DataTable from 'primevue/datatable';

import modelsService from '@/services/modelsService';
import useErrors from '@/hooks/useErrors';

import Yuri_Pavlovich_Sokolov from '@/assets/png/Yuri_Pavlovich_Sokolov.png';
import Janis_Ozolins from '@/assets/png/Janis_Ozolins.png'; 
import Jordan_Basketfield from '@/assets/png/Jordan_Basketfield.png'; 
import Nostradamus from '@/assets/png/Nostradamus.png';

const errors = useErrors();

const models = ref();

const loading = ref(false);

async function load() {
  loading.value = true;
  try {
    const response = await modelsService.getAllModels();
    if (response.status >= 200 && response.status < 300) {
      models.value = response.data;
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

function choseImage(id) {
  switch (id) {
    case 1:
      return Yuri_Pavlovich_Sokolov;
    case 3:
      return Janis_Ozolins;
    case 4:
      return Jordan_Basketfield;
    case 2:
      return Nostradamus;
    default:
      return Yuri_Pavlovich_Sokolov;
  }
}

function testFunc() {
  console.log('test');
}

</script>
<template>
  <div class="ba-main-form">
    <div class="ba-sticky-header">
      <h2>Models</h2>
    </div>
    <div class="ba-form-label">
      <p class="ba-description">Choose and click on model to get predictions from it</p>
    </div>

    <div class="models-card-wrapper">
      <div class="model-empty-wrapper" v-for="model in models" :key="model.id">
        <Card @click="testFunc" :allTimeAcc="66" :lastTimeAcc="30" :nominalAcc="50" :image="choseImage(model.id)">
          <template #header>{{ model.name }}</template>
        </Card>
        <div class="card-description">
          <h3>Description</h3>
          <div class="ba-data justify-text">{{ model.description }}</div>
        </div>
      </div>
    </div>
    <div class="ba-row ba-start-row">
      <p class="small-text">The development team is not responsible for anger AI or for your money if you decide to bet using our software</p>
    </div>
  </div>
</template>
  
