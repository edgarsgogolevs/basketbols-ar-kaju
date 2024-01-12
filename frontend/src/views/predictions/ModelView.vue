<script setup>
import { ref, onMounted } from 'vue';

import modelsService from '@/services/modelsService';
import useErrors from '@/hooks/useErrors';

import Chart from 'primevue/chart';
import GamesHistory from '@/components/GamesHistory.vue';

const props = defineProps({
    id: { type: Number}
});

const errors = useErrors();

const modelStandartDescription = ref('In the NBA, there is an indicator called PLUS_MINUS. This indicator can be positive or negative. It shows how well the team played overall. A team is taken and the average PLUS_MINUS is calculated when that team played at home. Then the opposing team is taken and the PLUS_MINUS is calculated, but when they are away. The difference between the matches between the two teams is then calculated. These radicals are used to train the model as input data X, and the win or loss is data Y. And so on for each game. Ready-made machine learning algorithms are used to make predictions.');
const usedAlgoritmName = ref('');
const usedAlgoritmText = ref('')
const usedImage = ref('');
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
    errors.pushNotification({ severity: 'error', summary: 'Unexepected error', detail: 'Probably your internet connection or our server lag. Please restart page', life: 30000 });
  } finally {
    loading.value = false;
  }
}

const modelStats = ref();
async function loadModelStats() {
  loading.value = true;
  try {
    const response = await modelsService.getModel(props.id);
    if (response.status >= 200 && response.status < 300) {
        modelStats.value = response.data;
    }

  } catch (error) {
    errors.pushNotification({ severity: 'error', summary: 'Unexepected error', detail: 'Probably your internet connection or our server lag. Please restart page', life: 30000 });
  } finally {
    loading.value = false;
  }
}
const games = ref();
async function loadModelHistory() {
  loading.value = true;
  try {
    const response = await modelsService.getModelHistory(props.id);
    if (response.status >= 200 && response.status < 300) {
        games.value = response.data.history;
    }
  } catch (error) {
    errors.pushNotification({ severity: 'error', summary: 'Unexepected error', detail: 'Probably your internet connection or our server lag. Please restart page', life: 30000 });
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
                data: [modelStats.value?.nominal_precision * 100],
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

function setModelData() {
  switch (props.id) {
    case 1:
        usedAlgoritmName.value = 'Support Vector Machine';
        usedAlgoritmText.value = 'Searches for the optimal hyperplane for separating classes in the data. The basic idea is to maximise the difference between classes using support vectors. The model is trained to find the optimal hyperplane with maximum spacing and can be used to predict whether new objects belong to classes.';
        usedImage.value = 'https://media.geeksforgeeks.org/wp-content/uploads/20231109124312/Hinge-loss-(2).png';
    return;
    case 2:
        usedAlgoritmName.value = 'Random Forest Classifier';
        usedAlgoritmText.value = 'Set up a decision tree group Each tree is trained using a random subsample of the data and random features. The voting of the trees leads the model to make a prediction on the new data. RandomForestClassifier is efficient, robust to overtraining and able to estimate the importance of features.';
        usedImage.value = 'https://media.geeksforgeeks.org/wp-content/uploads/20200516180708/Capture482.png';
    return;
    case 3:
        usedAlgoritmName.value = 'Logistic regression';
        usedAlgoritmText.value = 'Is inherited for binary classification. It creates an equation by combining the weights, converts it into a probability using a logistic function, and makes a decision based on that probability. The model is trained by optimising the weights so that its predictions are closer to the real data.';
        usedImage.value = 'https://miro.medium.com/v2/resize:fit:832/1*eMimR6WxLvcctZsvQ8UPIQ.png';
    return;
    case 4:
        usedAlgoritmName.value = 'XGBoost Classifier';
        usedAlgoritmText.value = 'Base uses many decision trees together. We give it the data and specify what we want to predict (whether a team will win or not). The model learns from this data, builds many trees, and each new tree tries to correct the mistakes of the previous trees. Eventually we have an ensemble of (many together) trees that work together to give an accurate prediction on the new data.';
        usedImage.value = 'https://media.geeksforgeeks.org/wp-content/uploads/20210707140911/Boosting.png';
    return;

    default:
        usedImage.value = 'https://media.geeksforgeeks.org/wp-content/uploads/20210707140911/Boosting.png';
    return;
  }

}

onMounted(() => {
    loadModel();
    loadModelStats();
    loadModelHistory();
    setTimeout(() => {
        chartData.value = setChartData();
        chartOptions.value = setChartOptions();
        setModelData();
    }, 1000);
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
        <div class="model-history">
            <div class="divider-with-line"></div>
            <h3>Model history</h3>
            <GamesHistory :games="games" />
        </div>
        <div class="model-schema">
            <div class="divider-with-line"></div>
            <h3>How model works</h3>
            <div class="schema-fades">
                <div v-animateonscroll="{ enterClass: 'fadein', leaveClass: 'fadeout' }" class="ba-data justify-text ba-description">
                    <div class="description-block">
                        <h4>Overall description</h4>
                        <p>{{ modelStandartDescription }}</p>
                    </div>
                </div>
                <div class="flex gap" v-animateonscroll="{ enterClass: 'fadein', leaveClass: 'fadeout' }">
                    <div v-animateonscroll="{ enterClass: 'fadeinleft', leaveClass: 'fadeoutleft' }"
                    class="algoritm-description animations">
                        <div class="column">
                            <i class="pi pi-spin pi-cog" style="font-size: 2rem"></i>
                            <h3 class="tiny">Algoritm</h3>
                            <h3 >{{ usedAlgoritmName }}</h3>
                        </div> 
                    </div>
                <div v-animateonscroll="{ enterClass: 'fadeinright', leaveClass: 'fadeoutright' }"
                 class="large-box animations">
                 <div class="badge">
                            <i class="pi pi-info-circle" style="font-size: 2rem"></i>
                        </div>
                    <p>{{ usedAlgoritmText }}</p>
                </div>
                </div>
                <div v-animateonscroll="{ enterClass: 'scalein', leaveClass: 'fadeout' }">
                    <div class="shema animations">
                        <h3>Schema</h3>
                        <img :src="usedImage" alt="shema" />
                    </div>
                </div>
            </div>
        </div>
    </div>
  </div>
</template>
