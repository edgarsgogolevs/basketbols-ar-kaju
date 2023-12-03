<script setup>
import { ref, computed } from 'vue';
import Knob from 'primevue/knob';
import Image from 'primevue/image';

const props = defineProps({
    allTimeAcc: { type: Number, default: null },
    lastTimeAcc: { type: Number, default: null },
    nominalAcc: { type: Number, default: null },
    image: { type: String, default: null }
});



const cardStyle = ref({});
const imageStyle = ref({ transform: 'scale(1)' });

function handleMouseMove(e) {
  let { offsetX: x, offsetY: y } = e;
  const { width, height } = e.target.getBoundingClientRect();

  x /= width;
  y /= height;

  x = (x - 0.5) * 10;
  y = (y - 0.5) * -10;

  cardStyle.value = {
    transform: `perspective(600px) rotateX(${y}deg) rotateY(${x}deg)`
  };
  imageStyle.value = {
    transform: `scale(1.2)`,
    transition: 'transform 0.3s'
  };
}
function handleMouseLeave() {
  cardStyle.value = {
    transform: `perspective(600px) rotateX(0deg) rotateY(0deg)`
  };
  imageStyle.value = {
    transform: `scale(1)`,
    transition: 'transform 0.3s'
  };
}
const allTime = ref(props.allTimeAcc);
const lastTime = ref(props.lastTimeAcc);
const nominal = ref(props.nominalAcc);

function knobColor(value) {
    let hue = ((value / 100) * 120).toString(10);
    let saturation = 80; 
    let lightness = 50;
    return ["hsl(", hue, ",", saturation + "%,", lightness + "%)"].join("");
};


</script>

<template>
  <div class="card" :style="cardStyle" @mousemove="handleMouseMove" @mouseleave="handleMouseLeave" @click="handleClick">
    <div class="card-header">
      <slot name="header"></slot>
    </div>
    <div class="card-content">
        <div class="knob-card" >
            <p>Prediction accuracy</p>
            <div class="flex-knob-block">
                <div>
                    <p>All time</p>
                    <Knob  v-model="allTime" :valueColor="knobColor(allTime)" readonly :valueTemplate="`${allTime}%`" />
                </div>
                <div>
                    <p>Last 10</p>
                    <Knob  v-model="lastTime" :valueColor="knobColor(lastTime)" readonly :valueTemplate="`${lastTime}%`" />
                </div>
                
            </div>
        </div>
        <div class="knob-card" >
            <p>Nominal</p>
            <Knob  v-model="nominal" :valueColor="knobColor(nominal)" readonly :valueTemplate="`${nominal}%`" />
        </div>
        <div class="card-image" :style="imageStyle" >
            <Image :src="image" alt="Image" width="100" />
        </div>
      <slot></slot>
    </div>
    <div class="card-footer">
      <slot name="footer"></slot>
    </div>
  </div>
</template>



<style scoped>
.card {
    display: flex;
    flex-direction: column;
    margin: 1rem;
    box-shadow: 0 0 11px rgb(35, 1, 69);
    border-radius: 4px;
    padding: 1rem;
    cursor: pointer;
    background-color: var(--color-area);
    transition: transform 0.1s; 
    transform-style: preserve-3d;
}
.card:hover {
    box-shadow: 0 0 11px var(--color-box-shadow-orange);
}

.card-header {
  font-weight: bold;
  margin-bottom: 0.5rem;
}
.card-content {
    min-height: 300px;
}

.card-footer {
  margin-top: 0.5rem;
}
.knob-card {
    margin-bottom: 0.5rem;
}
.card-image {
    height: 125px;
}
</style>
