<script setup>
import { ref, onMounted } from 'vue';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';

import testService from '@/services/testService';

const textValue = ref('Banan');


const selectedCity = ref({ name: 'Rome', code: 'RM' });
const cities = ref([
    { name: 'New York', code: 'NY' },
    { name: 'Rome', code: 'RM' },
    { name: 'London', code: 'LDN' },
    { name: 'Istanbul', code: 'IST' },
    { name: 'Paris', code: 'PRS' }
]);

const visible = ref(false);

function showDialog() {
  visible.value = true;
}

function load() {
  testService.getTest().then((response) => {
    // console.log(response);
  });
}

onMounted(() => {
  load();
});
const menu = ref();
const items = ref([
    {
        label: 'Options',
        items: [
            {
                label: 'Refresh',
                icon: 'pi pi-refresh'
            },
            {
                label: 'Export',
                icon: 'pi pi-upload'
            }
        ]
    }
]);

const toggle = (event) => {
    menu.value.toggle(event);
};

</script>
<template>
  <div class="ba-main-form form-2">
    <div class="ba-header">
      <h2>Games</h2>
    </div>
    <div class="ba-row">
      <div class="ba-row-flex " >
        <Button label="Primary" />
        <Button label="Secondary" severity="secondary" />
      </div>
    </div>
    <div class="ba-section-2">
    <div class="ba-row-2">
      <div class="ba-row-flex " >
        <InputText type="text" v-model="textValue" />
        <code>{{ textValue }}</code>
      </div>
    </div>
    <div class="ba-row-2">
      <div class="ba-row-flex " >
        <InputText type="text" v-model="textValue" />
        <code>{{ textValue }}</code>
      </div>
    </div>
  </div>
  </div>
</template>
  
