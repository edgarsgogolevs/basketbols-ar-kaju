<script setup>
import { ref, onMounted, watch } from 'vue';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import Dropdown from 'primevue/dropdown';
import Dialog from 'primevue/dialog';
import Menu from 'primevue/menu';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import ColumnGroup from 'primevue/columngroup';   
import Chart from 'primevue/chart';


import modelsService from '@/services/modelsService';

import GamesWidget from '@/components/GamesWidget.vue';

import useErrors from '@/hooks/useErrors';


const errors = useErrors();

const loading = ref(false);
const models = ref();
const recentModels = ref();
const upcommingModels = ref();
const teams = ref();

async function loadRecent() {
  loading.value = true;
  try {
    const response = await modelsService.getRecentGames(21);
    if (response.status >= 200 && response.status < 300) {
      recentModels.value = response.data;
    }
  } catch (error) {
    errors.pushNotification({ severity: 'error', summary: 'Unexepected error', detail: 'Probably your internet connection or our server lag. Please restart page', life: 30000 });
  } finally {
    loading.value = false;
  }
}
async function loadUpcoming() {
  loading.value = true;
  try {
    const response = await modelsService.getUpcomingGames(21);
    if (response.status >= 200 && response.status < 300) {
      upcommingModels.value = response.data;
    }
  } catch (error) {
    errors.pushNotification({ severity: 'error', summary: 'Unexepected error', detail: 'Probably your internet connection or our server lag. Please restart page', life: 30000 });
  } finally {
    loading.value = false;
  }
}
async function loadTeams() {
  loading.value = true;
  try {
    const response = await modelsService.getAllTeams();
    if (response.status >= 200 && response.status < 300) {
        teams.value = response.data;
    }

  } catch (error) {
    errors.pushNotification({ severity: 'error', summary: 'Unexepected error', detail: 'Probably your internet connection or our server lag. Please restart page', life: 30000 });
  } finally {
    loading.value = false;
  }
}

async function loadModels() {
  loading.value = true;
  try {
    const response = await modelsService.getAllModels();
    if (response.status >= 200 && response.status < 300) {
      models.value = response.data;

    }
  } catch (error) {
    errors.pushNotification({ severity: 'error', summary: 'Unexepected error', detail: 'Probably your internet connection or our server lag. Please restart page', life: 30000 });
  } finally {
    loading.value = false;
  }
}



const chartData = ref();
const chartOptions = ref();

watch(() => models.value,
  () => {
    chartData.value = setChartData();
    chartOptions.value = setChartOptions();
  }
);

onMounted(() => {
  loadRecent();
  loadUpcoming();
  loadTeams();
  loadModels();
});

function fillArrayOfAccuracties(id) {
  const array = [];
  if (!models.value) {
    return array;
  }
  
  switch (id) {
    case 1:
      for (let i = 0; i < models.value.length; i++) {
        array.push((models.value[i].all_time_accuracy*100).toFixed(2));
      }

      return array;
    case 2:
      for (let i = 0; i < models.value.length; i++) {
        array.push((models.value[i].last_ten_accuracy*100).toFixed(2));
      }

      return array;
    case 3:
      for (let i = 0; i < models.value.length; i++) {
        array.push((models.value[i].nominal_precision*100).toFixed(2));
      }

      return array;
    default:
      for (let i = 0; i < models.value.length; i++) {
        array.push((models.value[i].all_time_accuracy*100).toFixed(2));
      }

      return array;
  }
}

function setChartData() {
    return {
        labels: ['Yuri Pavlovich Sokolov', 'Nastradamus', 'Jānis Ozoliņš', 'Jordan Basketfield'],
        datasets: [
            {
                label: 'All time accuracy',
                data: fillArrayOfAccuracties(1),
                backgroundColor: 'rgba(255, 159, 64, 0.2)',
                borderColor: 'rgb(255, 159, 64)',
                borderWidth: 1
            },
            {
                label: 'Last 10 accuracy',
                data: fillArrayOfAccuracties(2),
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgb(75, 192, 192)',
                borderWidth: 1
            },
            {
                label: 'Nominal accuracy',
                data: fillArrayOfAccuracties(3),
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgb(54, 162, 235)',
                borderWidth: 1
            }
        ]
    };
};
function setChartOptions(){
    const documentStyle = getComputedStyle(document.documentElement);
    const textColor = documentStyle.getPropertyValue('--text-color');
    const textColorSecondary = documentStyle.getPropertyValue('--text-color-secondary');
    const surfaceBorder = documentStyle.getPropertyValue('--surface-border');
    return {
        plugins: {
            legend: {
                labels: {
                    color: textColor
                }
            }
        },
        scales: {
            x: {
                ticks: {
                    color: textColorSecondary
                },
                grid: {
                    color: surfaceBorder
                }
            },
            y: {
                min: 0,
                max: 100, 
                beginAtZero: true,
                ticks: {
                    color: textColorSecondary
                },
                grid: {
                    color: surfaceBorder
                }
            }
        }
    };
}


</script>
<template>
  <div class="ba-main-form">
    <div class="ba-sticky-header">
      <div></div>
      <h2>General</h2>
    </div>
    <div class="ba-section">
      <div class="games-viewer">
          <div class="recent-games">
            <GamesWidget :games="recentModels" :teams="teams" :recent="true" />
          </div>
          <div></div> 
          <div class="upcoming-games upcoming">
            <GamesWidget :games="upcommingModels" :teams="teams" :recent="false" />
          </div>
      </div>
    </div>
    <div class="ba-section">
      <h3>Models accuracy chart</h3>
      <div class="models-chart">
        <Chart type="bar" :data="chartData" :options="chartOptions" />
      </div>
    </div>
  </div>
</template>