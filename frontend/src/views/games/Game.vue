<script setup>
import { ref, onMounted, watch, computed } from 'vue';

import TabMenu from 'primevue/tabmenu';
import Accordion from 'primevue/accordion';
import AccordionTab from 'primevue/accordiontab';

import modelsService from '@/services/modelsService';
import Stats from '@/components/Stats.vue';
import Toast from 'primevue/toast';
import useErrors from '@/hooks/useErrors';
import { useToast } from 'primevue/usetoast';

import Skeleton from 'primevue/skeleton';
import ProgressBar from 'primevue/progressbar';

const errors = useErrors();


const props = defineProps({
    id: { type: Number}
});

const loading = ref(false);
const game = ref({});
const teams = ref();

async function loadGame() {
  loading.value = true;
  try {
    const response = await modelsService.getGame(props.id);
    if (response.status >= 200 && response.status < 300) {
        game.value = response.data;
    }
    console.log(game.value);
  } catch (error) {
    console.error(error);
    errors.pushNotification({ severity: 'error', summary: 'Unexepected error', detail: '111Probably your internet connection or our server lag', life: 30000 });
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

const predictionsArray = ref();

async function getPrediction(id) {
  loading.value = true;

  try {
    const response1 = await modelsService.getPrediction(id, 1);
    const response2 = await modelsService.getPrediction(id, 2);
    const response3 = await modelsService.getPrediction(id, 3);
    const response4 = await modelsService.getPrediction(id, 4);
    
    if (response1.status >= 200 && response1.status < 300 && response2.status >= 200 && response2.status < 300 && response3.status >= 200 && response3.status < 300 && response4.status >= 200 && response4.status < 300) {
        predictionsArray.value = [response1.data, response2.data, response3.data, response4.data];
    }
    
  } catch (error) {
    console.error(error)
    errors.pushNotification({ severity: 'error', summary: 'Unexepected error', detail: 'Probably your internet connection or our server lag', life: 30000 });
  } finally {
    loading.value = false;
  }
}
const models = ref();
async function loadModels() {
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

function findName(id) {
    if (!id) return 'N/A';
    const team = teams.value?.find(team => team.id === id);
    return team?.name;
}
function findLogo(id) {
    if (!id) return 'https://static.thenounproject.com/png/1738131-200.png';
    const team = teams.value?.find(team => team.id === id);
    return team?.logo_url;
}
function findAbbr(id) {
    if (!id) return 'N/A';
    const team = teams.value?.find(team => team.id === id);
    return team?.abbr;
}

function findModelById(id) {
    if (!id) return 'N/A';
    const model = models.value?.find(model => model.id === id);
    return model;
}

function formatDate(date) {
    const d = new Date(date);
    return d.toLocaleDateString();
}

const predictionsTempArray = ref([]);

function fillPredictionArray() {
    predictionsTempArray.value = predictionsArray.value;
}

function averageWinProbability() {
    let sum = 0;
    if (!predictionsArray.value) return 0;
    if (predictionsArray.value.length === 0) return 0;
    for (let i = 0; i < predictionsArray.value.length; i++) {
        sum += predictionsArray.value[i].home_winning_proba;
    }
    return sum / predictionsArray.value.length;
}
function checkIfLoading() {
    if (!predictionsTempArray.value) return;
    if (predictionsTempArray.value.length === 0) {
        loading.value = true;
    } else {
        loading.value = false;
    }
}

watch(() => game.value,
  () => {
    fillPredictionArray();
    checkIfLoading();
    averageWinProbability();
  }
);

onMounted(() => {
    loadTeams();
    loadGame();
    loadModels();
    getPrediction(props.id);
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
            <router-link to="/games">Games</router-link>
            </div>    
        </div>
        <h2>{{`Game - ${game?.id}`}}</h2>
    </div>
    <div class="ba-section big-game">
        <div>
                <i class="pi pi-calendar" style="font-size: 2rem" v-tooltip="formatDate(game.game_date)" type="text"></i>
            </div>
        <h3 class="no-margin">
            <span class="grid-row">
                <p class="team-home">{{ findName(game.team_home_id) }}</p>
                <p class="team-away">{{ findName(game.team_away_id) }}</p>
            </span>
        </h3>
        <div class="large-game-info">
            <p class="bold">{{ findAbbr(game.team_home_id) }}</p>
            
            <p class="bold">{{ findAbbr(game.team_away_id) }}</p>
        </div>
        <div class="large-game-info">
            <img alt="flag" :src="findLogo(game.team_home_id)" style="width: 320px" />
            <img alt="flag" :src="findLogo(game.team_away_id)" style="width: 320px" />
        </div>
        <div class="average-win-probability">
            <div class="flex">
                <p class="ba-primary">Win probability</p>
                <div class="ba-tooltip">
                    <i class="pi pi-info-circle" style="font-size: 1rem" v-tooltip="'Home team win chance'" type="text"></i>
                </div>
            </div>
            <ProgressBar :value="averageWinProbability().toFixed(2)*100"></ProgressBar>
        </div>
        <div class="divider-with-line"></div>
        <h3>Sepate model predictions</h3>
        <div v-if="!loading" class="predictions">
            <div v-for="item in predictionsArray" :key="item.model_id" class="prediction-card">
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
        <div class="divider-with-line"></div>
        <h3>Game stats</h3>
        <Accordion :activeIndex="1" v-if="game.MIN">
            <AccordionTab header="Open stats">
                <Stats :game="game" />
            </AccordionTab>
        </Accordion>
        <div v-else>Not available for the upcoming game</div>
    </div>
  </div>
</template>
<style>

.big-game .prediction-card {
    padding: 2rem;
}
.big-game .probability.ba-description {
    margin-bottom: 1rem;
}
.no-margin {
    margin-bottom: 0;
}
.large-game-info {
    display: grid;
    grid-template-columns: 1fr 1fr;
    justify-items: center; 
    align-items: center;
    margin-bottom: 1rem;
}
.large-game-info-3 {
    display: grid;
    grid-template-columns: 99fr 1fr 99fr;
    justify-items: center; 
    align-items: center;
    margin-bottom: 1rem;
}
.ba-section h3 .grid {
    align-self: center;
}
.grid-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
}
</style>