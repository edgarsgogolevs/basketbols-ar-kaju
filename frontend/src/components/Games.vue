<script setup>
import { ref, computed, onMounted,withDirectives  } from 'vue';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button';
import Tooltip from 'primevue/tooltip';
import Dialog from 'primevue/dialog';

import useErrors from '@/hooks/useErrors';
import modelsService from '@/services/modelsService';
import router from '@/router';

import SmallPrediction from '@/components/SmallPrediction.vue';

const errors = useErrors();

const props = defineProps({
    games: { type: Array, default: null },
});

const loading = ref(false);
const teams = ref();

async function loadTeams() {
  loading.value = true;
  try {
    const response = await modelsService.getAllTeams();
    if (response.status >= 200 && response.status < 300) {
        teams.value = response.data;
    }

  } catch (error) {
    errors.pushNotification({ severity: 'error', summary: 'Unexepected error', detail: 'Probably your internet connection or our server lag. Please restart page. Please restart page', life: 30000 });
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
    errors.pushNotification({ severity: 'error', summary: 'Unexepected error', detail: 'Probably your internet connection or our server lag. Please restart page', life: 30000 });
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
    errors.pushNotification({ severity: 'error', summary: 'Unexepected error', detail: 'Probably your internet connection or our server lag. Please restart page', life: 30000 });
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
     loadTeams();
     loadModels();
});

function findLogo(id) {
    if (!id) return 'https://static.thenounproject.com/png/1738131-200.png';
    const team = teams.value?.find(team => team.id === id);
    return team?.logo_url;
}
function findName(id) {
    if (!id) return 'N/A';
    const team = teams.value?.find(team => team.id === id);
    return team?.name;
}

function findAbbr(id) {
    if (!id) return 'N/A';
    const team = teams.value?.find(team => team.id === id);
    return team?.abbr;
}
function concateAbbr(home, away) {
    return findAbbr(home) + ' VS ' + findAbbr(away);
}
function concateName(home, away) {
    return findName(home) + ' VS ' + findName(away);
}
function findConference(id) {
    if (!id) return 'N/A';
    const team = teams.value?.find(team => team.id === id);
    return team.conference;
}

function formatDate(date) {
    const d = new Date(date);
    return d.toLocaleDateString();
}

function goToGame(id) {

    router.push({ name: 'game', params: { id: id } });
}

const visible = ref(false);
const modalItem = ref(null)

function showDialog(item) {
    modalItem.value = item;
    getPrediction(item.id);
    visible.value = true;
}

function formatScore(score) {
    if (!score) return 'N/A';
    return score;
}
function calculateClass(homeWon, check) {
    if (!check) {
      return 'bold';
    }
    if (homeWon === undefined || homeWon === null) {
      return 'bold';
    }
    return homeWon ? 'winner' : 'loser';
}

</script>

<template>
    <div>
        <DataTable :value="props.games" paginator :rows="20" :loading="loading" :rowsPerPageOptions="[5, 10, 20, 50]" tableStyle="min-width: 50rem">
            <template #loading> Loading customers data. Please wait. </template>
            <Column field="id" header="Game id" sortable style="width: 5%">
                <template #body="item">
                    <p class="grid-link" @click="goToGame(item.data.id)">{{ item.data.id }}</p>
                </template>
            </Column>
            <Column field="game_date" header="Date" sortable style="width: 5%">
                <template #body="item">
                    <p>{{ formatDate(item.data.game_date) }}</p>
                </template>
            </Column>
            <Column field="team_home_id" sortable header="Team home id" style="width: 8%"></Column>
            <Column field="team_away_id" sortable header="Team away id" style="width: 8%"></Column>
            <Column field="Match_between" header="Match between" style="width: 10%">
                <template #body="item">
                <div class="flex align-items-center gap-2">
                        <img alt="flag" :src="findLogo(item.data.team_home_id)" style="width: 40px" />
                        <p>VS</p>
                        <img alt="flag" :src="findLogo(item.data.team_away_id)" style="width: 40px" />
                    </div>
                </template>
            </Column>
            <Column field="team_home_id" sortable header="Home vs Away" style="width: 25%">
                <template #body="item">
                    <div class="flex align-items-center gap-2">
                        <p class="team-home">{{ findName(item.data.team_home_id) }}</p>
                        <p>VS</p>
                        <p class="team-away">{{ findName(item.data.team_away_id) }}</p>
                    </div>
                </template>
            </Column>
            <Column field="buttons"  header="" style="width: 8%">
                <template #body="item"> 
                    <span class="p-buttonset">
                        <Button v-tooltip="'Open quick prediction'" outlined icon="pi pi-external-link" severity="Secondary" aria-label="Submit" @click="showDialog(item.data)" />
                        <Button v-tooltip="'Open game page'" outlined icon="pi pi-arrow-right" severity="Secondary" aria-label="Submit" @click="goToGame(item.data.id)" />
                    </span> 
                </template>
            </Column>
        </DataTable>
        <Dialog v-model:visible="visible" modal  :style="{ width: '50rem' }" :breakpoints="{ '1199px': '75vw', '575px': '90vw' }">
            <template #header>
                <p>{{ `Game: ${concateAbbr(modalItem?.team_home_id, modalItem?.team_away_id)} (${modalItem.id})`}}</p>
            </template>
            <div class="modal-team-names">
                <div>
                    <p class="team-pos">Home</p>
                <p class="team-conference" :class="[{ 'west': findConference(modalItem.team_home_id) === 'West'},
                { 'east': findConference(modalItem.team_home_id) === 'East'}]">{{ findName(modalItem?.team_home_id) }}</p>
                </div>
                <p></p>
                <div>
                    <p class="team-pos">Away</p>
                <p class="team-conference" :class="[{ 'west': findConference(modalItem.team_away_id) === 'West'},
                { 'east': findConference(modalItem.team_away_id) === 'East'}]">{{ findName(modalItem?.team_away_id) }}</p>
                </div>
            </div>
            <div class="modal-team-logos">
                <img alt="flag" :src="findLogo(modalItem.team_home_id)" style="width: 120px" />
                <p class="versus">VS</p>
                <img alt="flag" :src="findLogo(modalItem.team_away_id)" style="width: 120px" />
            </div>

            <div class="quick-score">
                <p>Home score: <span class="bold" :class="calculateClass(modalItem.home_won, modalItem.score_home)">{{ formatScore(modalItem.score_home) }}</span></p>
                <i class="pi pi-calendar" style="font-size: 2rem" v-tooltip="formatDate(modalItem.game_date)" type="text"></i>
                <p>Away score: <span class="bold" :class="calculateClass(!modalItem.home_won, modalItem.score_home)">{{ formatScore(modalItem.score_away) }}</span></p> 
            </div>
            <div class="prediction-info">
                <SmallPrediction :predictions="predictionsArray" :models="models" />
            </div>
            <template #footer>
                <Button label="Close" severity="secondary" @click="visible = false"  />
                <Button label="Open game page" severity="primary"  @click="visible = false, goToGame(modalItem.id)" />
            </template>
        </Dialog>
    </div>
</template>