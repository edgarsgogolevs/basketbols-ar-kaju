<script setup>
import { ref, onMounted } from 'vue';

import modelsService from '@/services/modelsService';
import useErrors from '@/hooks/useErrors';

import Chart from 'primevue/chart';

const props = defineProps({
    id: { type: Number}
});

const errors = useErrors();

const model = ref();

const loading = ref(false);

async function loadModel() {
  loading.value = true;
  try {
    const response = await modelsService.getModelById(props.id);
    if (response.status >= 200 && response.status < 300) {
      model.value = response.data;
    }
  } catch (error) {
    errors.pushNotification({ severity: 'error', summary: 'Unexepected error', detail: 'Probably your internet connection or our server lag', life: 30000 });
  } finally {
    loading.value = false;
  }
}

const modelStats = ref();
async function loadModelStats() {
  loading.value = true;
  try {
    const response = await modelsService.getModelStats(props.id);
    if (response.status >= 200 && response.status < 300) {
        modelStats.value = response.data;
    }
    console.log(response.data);

  } catch (error) {
    errors.pushNotification({ severity: 'error', summary: 'Unexepected error', detail: 'Probably your internet connection or our server lag', life: 30000 });
  } finally {
    loading.value = false;
  }
}

const chartData = ref();
const chartOptions = ref();

function setChartData() {
    return {
        labels: [''],
        datasets: [
            {
                label: 'All time accuracy %',
                data: [modelStats.value?.all_time_accuracy * 100],
                backgroundColor: 'rgba(255, 159, 64, 0.2)',
                borderColor: 'rgb(255, 159, 64)',
                borderWidth: 1
            },
            {
                label: 'Last 10 accuracy %',
                data: [modelStats.value?.last_ten_accuracy * 100],
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgb(75, 192, 192)',
                borderWidth: 1
            },
            {
                label: 'Nominal accuracy %',
                data: [modelStats.value?.nominal_accuracy * 100],
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgb(54, 162, 235)',
                borderWidth: 1
            }
        ]
    };
};
function setChartOptions() {
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

onMounted(() => {
    loadModel();
    loadModelStats();

    setTimeout(() => {
        chartData.value = setChartData();
        chartOptions.value = setChartOptions();
    }, 300);
});

</script>
<template>
  <div class="ba-main-form">
    <div class="ba-sticky-header">
    <div class="breadcrumbs">
        <div class="breadcrumb-separator">
            <i class="pi pi-home"></i>
        </div> 
        <div class="breadcrumbs-item">
          <router-link to="/">Home</router-link>
        </div>
        <div class="breadcrumb-separator">
            <i class="pi pi-chevron-right"></i>
        </div>   
        <div class="breadcrumbs-item">
          <router-link to="/models">Models</router-link>
        </div>    
    </div>
      <h2>{{ model?.name }}</h2>
    </div>
    <div class="ba-section padding-top-2">
        <div class="model-card">
            <div class="model-image">
                <img :src="model?.profile_picture" alt="model image" />
            </div>
            <div class="card-description">
                <h3>Stats</h3>
                <div class="models-chart">
                    <Chart type="bar" :data="chartData" :options="chartOptions" />
                </div>
                <h3>Description</h3>
                <div class="ba-data justify-text ba-description">{{ model?.description }}</div>
            </div>
        </div>
    </div>
  </div>
</template>
<style>
.padding-top-2 {
    padding-top: 2rem;
}
.model-image>img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 15px;
}
.model-card {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-gap: 1rem;
    align-items: center;
    justify-items: center;
}
</style>