<script setup>
import { ref, onMounted } from 'vue';
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
    errors.pushNotification({ severity: 'error', summary: 'Unexepected error', detail: 'Probably your internet connection or our server lag', life: 30000 });
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
    errors.pushNotification({ severity: 'error', summary: 'Unexepected error', detail: 'Probably your internet connection or our server lag', life: 30000 });
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
    errors.pushNotification({ severity: 'error', summary: 'Unexepected error', detail: 'Probably your internet connection or our server lag', life: 30000 });
  } finally {
    loading.value = false;
  }
}



const chartData = ref();
const chartOptions = ref();

onMounted(() => {

  loadRecent();
  loadUpcoming();
  loadTeams();

  chartData.value = setChartData();
  chartOptions.value = setChartOptions();
});

const setChartData = () => {
    return {
        labels: ['Yuri Pavlovich Sokolov', 'Nastradamus', 'Jānis Ozoliņš', 'Jordan Basketfield'],
        datasets: [
            {
                label: 'All time accuracy',
                data: [51, 23, 69, 99],
                backgroundColor: 'rgba(255, 159, 64, 0.2)',
                borderColor: 'rgb(255, 159, 64)',
                borderWidth: 1
            },
            {
                label: 'Last 10 accuracy',
                data: [41, 33, 59, 89],
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgb(75, 192, 192)',
                borderWidth: 1
            },
            {
                label: 'Nominal accuracy',
                data: [31, 43, 49, 79],
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgb(54, 162, 235)',
                borderWidth: 1
            }
        ]
    };
};
const setChartOptions = () => {
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
<style>

.models-chart {
  margin: 1rem;
  padding: 1rem;
  border: 2px solid var(--surface-border);
  border-radius: 15px;
}
.games-viewer {
  display: grid;
  justify-items: center; 
  align-items: center; 
  grid-template-columns: 1fr auto 1fr;
}
.games-viewer .recent-games {
  justify-self: start; 
  align-items: start;
}
.games-viewer .upcoming-games {
  justify-self: end; 
  align-items: end;
}
.recent-games,
.upcoming-games {
    width: 700px;
}
</style>
