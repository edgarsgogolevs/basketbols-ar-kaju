<script setup>
import { ref, computed, onMounted } from 'vue';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button';

import useErrors from '@/hooks/useErrors';
import modelsService from '@/services/modelsService';
import router from '@/router';

const errors = useErrors();

const props = defineProps({
    games: { type: Array, default: null },
    upcoming: { type: Number, default: 0 }
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
    errors.pushNotification({ severity: 'error', summary: 'Unexepected error', detail: 'Probably your internet connection or our server lag', life: 30000 });
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
     loadTeams();
});

function findLogo(id) {
    const team = teams.value?.find(team => team.id === id);
    return team.logo_url;
}
function findName(id) {
    const team = teams.value?.find(team => team.id === id);
    return team.name;
}

function formatDate(date) {
    const d = new Date(date);
    return d.toLocaleDateString();
}

function predictGame(game) {
    router.push({ name: 'predict', params: { id: game.id, home: game.team_home_id, away: game.team_away_id } });
}

</script>

<template>
    <div>
        <DataTable :value="props.games" paginator :rows="20" :loading="loading" :rowsPerPageOptions="[5, 10, 20, 50]" tableStyle="min-width: 50rem">
            <template #loading> Loading customers data. Please wait. </template>
            <Column field="game_date" header="Date" style="width: 5%">
                <template #body="item">
                    <p>{{ formatDate(item.data.game_date) }}</p>
                </template>
            </Column>
            <Column field="id" header="Game id" style="width: 5%"></Column>
            <Column field="team_away_id" header="Team away id" style="width: 8%"></Column>
            <Column field="team_home_id" header="Team home id" style="width: 8%"></Column>
            <Column field="team_home_id" header="Match between" style="width: 10%">
                <template #body="item">
                    <div class="flex align-items-center gap-2">
                        <img alt="flag" :src="findLogo(item.data.team_home_id)" style="width: 40px" />
                        <p>VS</p>
                        <img alt="flag" :src="findLogo(item.data.team_away_id)" style="width: 40px" />
                    </div>
                </template>
            </Column>
            <Column field="team_home_id" header="Home vs Away" style="width: 25%">
                <template #body="item">
                    <div class="flex align-items-center gap-2">
                        <p class="team-home">{{ findName(item.data.team_home_id) }}</p>
                        <p>VS</p>
                        <p class="team-away">{{ findName(item.data.team_away_id) }}</p>
                    </div>
                </template>
            </Column>
            <Column v-if="upcoming === 0" field="team_home_id" header="Result" style="width: 8%"></Column>
            <Column v-if="upcoming === 1" field="team_home_id" header="Prediction" style="width: 5%">
                <template #body="item">
                    <Button label="Predict" severity="Primary" @click="predictGame(item.data)" />
                </template>
            </Column>
        </DataTable>
    </div>
</template>

<style>
.team-home {
    color: #1e90ff;
}
.team-away {
    color: #ff4500;
}
</style>