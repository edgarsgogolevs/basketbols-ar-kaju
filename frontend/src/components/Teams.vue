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