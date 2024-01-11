<script setup>
import Accordion from 'primevue/accordion';
import AccordionTab from 'primevue/accordiontab';
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
        <div class="team" v-for="item in props.teams" :key="item.id">
            <div class="team-card">
            <h2 class="team-name">{{ item.name }}</h2>
            <img :src="item.logo_url" :alt="item.name" class="team-logo">
            <p class="team-abbr">{{ item.abbr }}</p>
            <div class="team-home-info">
                <div class="flex">
                    <i class="mdi mdi-map-marker-outline mdi-36px color-brand-icon"></i>
                    <p class="team-conference" :class="[{ 'west': item.conference === 'West'},
                    { 'east': item.conference === 'East'}]">
                    {{ item.conference }} coast
                    </p>
                </div>
                <div class="flex">
                    <i class="mdi mdi-city mdi-36px color-brand-icon"></i>
                    <p class="bold">
                    {{ item.town }}
                    </p>
                </div>
            </div>
            <Accordion :activeIndex="1">
                <AccordionTab header="Description">
                    <p class="ba-description">{{ item.description }}</p>
                </AccordionTab>
            </Accordion>
            <div class="divider"></div>
            <Button @click="goTO(item.nba_url)" label="Visit team page" severity="secondary" raised />
    </div>
        </div>
    </div>
</template>
<style>
.divider {
    margin-top: 1rem;
    margin-bottom: 1rem;
}
.team-home-info>.flex>i {
    margin: 0.5rem;
}
.color-brand-icon {
    color: var(--color-brand-icon)
}
.team-home-info {
    display: grid;
    grid-template-columns: 1fr 1fr;
    justify-items: center;
    margin-bottom: 0.5rem;
    margin-top: 0.5rem;
}
.team-home-info .team-conference {
    margin: 0;
}
.flex {
    display: flex;
    align-items: center;
}
.bold {
    font-weight: bold;
}
</style>
