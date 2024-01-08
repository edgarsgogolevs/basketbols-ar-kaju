<script setup>
import { ref, computed } from 'vue';
import Button from 'primevue/button';

const props = defineProps({
    teams: { type: Array, default: null },
});


</script>

<template>
    <div class="ba-teams-grid">
        <div class="team" v-for="item in props.teams" :key="item.id">
            <div class="team-card">
            <h2 class="team-name">{{ item.name }}</h2>
            <img :src="item.logo_url" :alt="item.name" class="team-logo">
            <p class="team-abbr">{{ item.abbr }}</p>
            <p class="team-conference" :class="[{ 'west': item.conference === 'West'},
                { 'east': item.conference === 'East'}]">
                {{ item.conference }}
            </p>
            <p class="team-description">{{ item.description }}</p>
            <a :href="item.nba_url" class="team-link">Visit NBA Page</a>
    </div>
        </div>
    </div>
</template>
<style>
.ba-teams-grid {
    padding: 1rem;
    display: grid;
    width: auto;
    grid-template-columns: repeat(3, 1fr);
    grid-gap: 1rem;
}
.team {
    /* border: 2px solid red; */
}

.team-card {
    border: 1px solid var(--color-border);
    padding: 1rem;
    margin-bottom: 1rem;
}
.team-logo {
    width: 100px;
    height: 100px;
}
.team-name {
    font-size: 1.5rem;
    font-weight: bold;
}
.team-abbr {
    font-size: 1.2rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
    margin-top: 1rem;
    color: var(--color-text);
}
.team-conference {
    font-size: 1rem;
    margin-bottom: 0.5rem;
    font-weight: bold;
}
.team-conference.east {
    color: var(--color-east-coast-text);
}
.team-conference.west {
    color: var(--color-west-coast-text);
}
.team-description {
    font-size: 0.9rem;
    margin-bottom: 1rem;
}
.team-link {
    color: blue;
    text-decoration: none;
}
</style>
