<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

function toSandbox() {
  router.push('sandbox')
}
</script>
<template>
  <div>
    <button @click="toSandbox">Sandbox</button>
  </div>
</template>
  

  