<script setup>
import { ref, computed } from 'vue'
const props = defineProps({
  msg: String
})

const showLess = ref(true)


</script>

<template>
  <div v-if="!showLess" v-html="msg"></div>
  <a @click="showLess = !showLess">
    {{ showLess ? 'Learn More' : 'Show Less' }}
  </a>
</template>

<style scoped>
  a {
    cursor: pointer;
  }
  p {
    padding-top: 10px;
  }
</style>
