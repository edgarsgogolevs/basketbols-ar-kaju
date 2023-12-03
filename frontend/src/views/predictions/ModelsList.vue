<script setup>
import { ref, onMounted } from 'vue';

import Card from '@/components/Card.vue';
import testService from '@/services/testService';
import useErrors from '@/hooks/useErrors';

import amogus from '@/assets/png/amogus.png';
import mcfly from '@/assets/png/mcfly.png'; 
import skynet from '@/assets/png/skynet4.png'; 
import nastra from '@/assets/png/nastradamus.png'; 
const errors = useErrors();


const loading = ref(false);

async function load() {
  loading.value = true;
  try {
    const response = await testService.getTest();
    
    if (response.status >= 200 && response.status < 300) {
      dataTemp.value = response.data;
    }
    // dataTemp.value = response.data;
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
      <h2>Models</h2>
    </div>
    <div class="ba-form-label">
      <p class="ba-description">Choose and click on model to get predictions from it</p>
    </div>

    <div class="models-card-wrapper">
      <Card :allTimeAcc="66" :lastTimeAcc="30" :nominalAcc="50" :image="amogus">
        <template #header>SUS Prognostic Predictor</template>
        <template #footer>Fast and fairly accurate model, but sus...</template>
      </Card>
      <Card :allTimeAcc="76"  :lastTimeAcc="40" :nominalAcc="30" :image="mcfly">
        <template #header>Biff Tannen</template>
        <template #footer>There's a rumour that he stole a Sports Almanac from the future</template>
      </Card>
      <Card :allTimeAcc="15"  :lastTimeAcc="10" :nominalAcc="25" :image="nastra">
        <template #header>Nastradambus</template>
        <template #footer>As the years go by his predictions are still based on pointing a finger at sky</template>
      </Card>
      <Card :allTimeAcc="100"  :lastTimeAcc="90" :nominalAcc="85" :image="skynet">
        <template #header>SKYNET / HAL9000</template>
        <template #footer>Two powerful AIs capable of wiping mankind out, if they can handle with reCAPTCHA, of course.</template>
      </Card>
    </div>
    <div class="ba-row ba-start-row">
      <p class="small-text">The development team is not responsible for anger AI or for your money if you decide to bet using our software</p>
    </div>
    </div>

</template>
  
