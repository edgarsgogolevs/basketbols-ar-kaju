<script setup>
import { ref, computed } from 'vue';
import Button from 'primevue/button';

const props = defineProps({
    teams: { type: Array, default: null },
});


function goTO(link) {
  window.open(link, '_blank');
}

</script>

<template>
    <div class="ba-teams-grid">
        <div class="team" v-for="item in props.teams" :key="item.id" @click="goTO(item.nba_url)">
            <div class="team-card">
            <h2 class="team-name">{{ item.name }}</h2>
            <img :src="item.logo_url" :alt="item.name" class="team-logo">
            <p class="team-abbr">{{ item.abbr }}</p>
            <p class="team-conference" :class="[{ 'west': item.conference === 'West'},
                { 'east': item.conference === 'East'}]">
                {{ item.conference }}
            </p>
            <p class="team-description">{{ item.description }}</p>
            <a :href="item.nba_url" class="team-link">Click to visit NBA Page</a>
    </div>
        </div>
    </div>
</template>
<style>

</style>
