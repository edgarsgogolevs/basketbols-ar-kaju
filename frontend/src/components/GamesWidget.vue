<script setup>
import { ref, computed } from 'vue';
import Button from 'primevue/button';
import Carousel from 'primevue/carousel';

import router from '@/router';


const props = defineProps({
    games: { type: Array, default: null },
    recent: { type: Boolean, default: true },
    teams: { type: Array, default: null },
});

const responsiveOptions = ref([
    {
        breakpoint: '100px',
        numVisible: 2,
        numScroll: 1
    },
    {
        breakpoint: '200px',
        numVisible: 3,
        numScroll: 1
    },
    {
        breakpoint: '300px',
        numVisible: 2,
        numScroll: 1
    },
    {
        breakpoint: '400px',
        numVisible: 1,
        numScroll: 1
    }
]);

function findLogo(id) {
    if (!id) return 'https://static.thenounproject.com/png/1738131-200.png';
    const team = props.teams?.find(team => team.id === id);
    return team?.logo_url;
}

function findAbbr(id) {
    if (!id) return 'N/A';
    const team = props.teams?.find(team => team.id === id);
    return team?.abbr;
}
function findConference(id) {
    if (!id) return 'N/A';
    const team = props.teams?.find(team => team.id === id);
    return team?.conference;
}

function formatDate(date) {

    const d = new Date(date);
    return d.toLocaleDateString();
}

function goToGame(id) {
    router.push({ name: 'game', params: { id: id } });
}

</script>

<template>
    <div class="games-widget">
        <div class="games-widget-header">
            <p v-if="recent">Recent games</p>
            <p v-else>Upcoming games</p>
        </div>
        <Carousel :value="props.games" :numVisible="3" circular :autoplayInterval="5000" :numScroll="3" :responsiveOptions="responsiveOptions">
            <template #item="slotProps">
                <div class="border-1 surface-border border-round m-2 text-center py-5 px-3">
                    <div class="flex align-items-center gap-2 fixed-height-60">
                        <img :src="findLogo(slotProps.data.team_home_id)" :alt="slotProps.data.name" class="w-6 shadow-2" />
                        <p class="versus">VS</p>
                        <img :src="findLogo(slotProps.data.team_away_id)" :alt="slotProps.data.name" class="w-6 shadow-2" />
                    </div>
                    <div class="widget-data">
                        <div class="game-abbr-grid">
                            <p class="team-conference"
                             :class="[{ 'west': findConference(slotProps.data.team_home_id) === 'West'},
                            { 'east': findConference(slotProps.data.team_home_id) === 'East'}]">
                            {{ findAbbr(slotProps.data.team_home_id) }}
                            </p>
                            <p></p>
                            <p class="team-conference"
                            :class="[{ 'west': findConference(slotProps.data.team_away_id) === 'West'},
                            { 'east': findConference(slotProps.data.team_away_id) === 'East'}]">
                             {{findAbbr(slotProps.data.team_away_id)}}
                            </p>
                        </div>
                        <div class="addition-info">
                            <p class="game-date">{{ formatDate(slotProps.data.game_date) }}</p>
                            <p class="game-id">Game id: {{ slotProps.data.id }}</p>
                        </div>

                        <div class="mt-5 flex align-items-center justify-content-center gap-2">
                            <Button icon="pi pi-external-link" severity="secondary" rounded outlined aria-label="Search" @click="goToGame(slotProps.data.id)" />
                        </div>
                    </div>
                </div>
            </template>
        </Carousel>
    </div>
</template>
<style>
.p-carousel-item>.border-1 {
    height: 300px;
    background-color: var(--color-area);
}
.addition-info {
    margin-top: 1.5rem;
}
.game-date {
    margin-bottom: 0.5rem;
    font-weight: 500;
}
.flex.align-items-center.gap-2.fixed-height-50 {
    height: 60px;
}
.game-abbr-grid .team-conference {
    margin-top: 1rem;
}
.game-abbr-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    justify-items: center;
    align-items: center;
}

.games-widget-header {
    font-size: 1.1rem;
    font-weight: bold;
    margin-bottom: 1rem;
    margin-top: 0.5rem;
}
</style>
