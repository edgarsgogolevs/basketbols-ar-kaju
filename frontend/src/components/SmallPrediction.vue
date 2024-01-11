<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import Knob from 'primevue/knob';
import Image from 'primevue/image';

import ProgressBar from 'primevue/progressbar';

import Skeleton from 'primevue/skeleton';

const props = defineProps({
    predictions: { type: Array, default: null },
    models: { type: Array, default: null },
});

function findModelById(id) {
    if (!id) return 'N/A';
    const model = props.models?.find(model => model.id === id);
    return model;
}

const predictionsTempArray = ref([]);

function fillPredictionArray() {
    for (let i = 0; i < props.predictions.length; i++) {
        predictionsTempArray.value.push(props.predictions[i]);
    }
}

function averageWinProbability() {
    let sum = 0;
    if (predictionsTempArray.value.length === 0) return 0;
    for (let i = 0; i < props.predictions.length; i++) {
        sum += props.predictions[i].home_winning_proba;
    }
    return sum / props.predictions.length;
}
const loading = ref(true);

function checkIfLoading() {
    if (props.predictions.length === 0) {
        loading.value = true;
    } else {
        loading.value = false;
    }
}

watch(() => props.predictions,
  () => {
    fillPredictionArray();
    checkIfLoading();
  }
);

</script>

<template>
    <div class="predictions-wrapper">
        <div class="average-win-probability">
            <div class="flex">
                <p class="ba-primary">Win probability</p>
                <div class="ba-tooltip">
                    <i class="pi pi-info-circle" style="font-size: 1rem" v-tooltip="'Home team win chance'" type="text"></i>
                </div>
            </div>
            <ProgressBar :value="averageWinProbability().toFixed(2)*100"></ProgressBar>
        </div>
        <p >Separate model predictions</p>
        <div v-if="!loading" class="predictions">
            <div v-for="item in predictions" :key="item.model_id" class="prediction-card">
                <div class="card-header">
                    {{ findModelById(item.model_id).name  }}
                </div>
                <div class="card-prediction">
                    <p class="probability ba-description" >Chance of home winning</p>
                    <ProgressBar v-tooltip="`${(item.home_winning_proba * 100).toFixed(2)}%`" type="text" placeholder="Top" :value="(item.home_winning_proba * 100).toFixed(0)" ></ProgressBar>
                </div>
            </div>
        </div>
        <div v-else class="predictions">
            <Skeleton width="10rem" height="4rem" borderRadius="16px"></Skeleton>
            <Skeleton width="10rem" height="4rem" borderRadius="16px"></Skeleton>
            <Skeleton width="10rem" height="4rem" borderRadius="16px"></Skeleton>
            <Skeleton width="10rem" height="4rem" borderRadius="16px"></Skeleton>
        </div>
    </div>
</template>
