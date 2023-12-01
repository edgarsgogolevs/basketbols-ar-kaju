<script setup>
import { ref, onMounted } from 'vue';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import Dropdown from 'primevue/dropdown';
import Dialog from 'primevue/dialog';
import Menu from 'primevue/menu';

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
    console.log(response);
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
  <div class="ba-main-form">
    <div class="ba-header">
      <h1>Sandbox</h1>
    </div>
    <div class="ba-row">
      <div class="ba-page-header">
        <h2>Button</h2>


      </div>
      <div class="ba-page-body" >
        <Button label="Primary" />
        <Button label="Secondary" severity="secondary" />
        <Button label="Success" severity="success" />
        <Button label="Info" severity="info" />
        <Button label="Warning" severity="warning" />
        <Button label="Help" severity="help" />
        <Button label="Danger" severity="danger" />
      </div>
    </div>
    <div class="ba-row">
      <div class="ba-page-header">
        <h2>InputText</h2>
      </div>
      <div class="ba-page-body" >
        <InputText type="text" v-model="textValue" />
        <code>{{ textValue }}</code>
      </div>
    </div>
    <div class="ba-row">
      <div class="ba-page-header">
        <h2>Value picker</h2>
      </div>
      <div class="ba-page-body" >
        <Dropdown v-model="selectedCity" :options="cities" optionLabel="name" placeholder="Select a City" class="w-full md:w-14rem" />
      <code>{{ selectedCity?.name }}</code>
      </div>
    </div>
    <div class="ba-row">
      <div class="ba-page-header">
        <h2>Dialog</h2>
      </div>
      <div class="ba-page-body" >
        <Button label="Show" icon="pi pi-external-link" @click="showDialog" />
        
        <Dialog v-model:visible="visible" modal header="Header" :style="{ width: '50rem' }" :breakpoints="{ '1199px': '75vw', '575px': '90vw' }">
              <p>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                  Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
                    Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
              </p>
        </Dialog>
        <code>{{ visible }}</code>
      </div>
    </div>
    <div class="ba-row">
      <div class="ba-page-header">
        <h2>Menu</h2>
      </div>
      <div class="ba-page-body" >
        <div class="card flex justify-content-center">
        <Button type="button" icon="pi pi-ellipsis-v" @click="toggle" aria-haspopup="true" aria-controls="overlay_menu" />
        <Menu ref="menu" id="overlay_menu" :model="items" :popup="true" />
    </div>
      </div>
    </div>  
  </div>
</template>
  
