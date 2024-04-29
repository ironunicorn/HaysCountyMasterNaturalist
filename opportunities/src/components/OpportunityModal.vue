<script setup>
import { ref, computed } from 'vue'

import { getCategory, formatDateDisplay } from '../utils.js'

const props = defineProps({
  opp: Object
})

function close() {
  props.opp = {}
}

</script>

<template>
  <div class="modal-container" v-if="props.opp.title">
    <div class="modal">
      <span class="close" @click="close">&times;</span>
      <div class="opp-wrapper">
        <h2>{{ props.opp.title }}</h2>
        <div style="font-weight:bold;">{{ formatDateDisplay(opp) }}</div>
        <div><i>{{ props.opp.anywhere ? 'Anywhere' : props.opp.location }}</i></div>
        <div v-if="props.opp.category === 'AT'"><b>AT: {{ props.opp.project_id }}</b></div>
        <div v-else-if="props.opp.category === 'EV'"><b>{{ props.opp.project_id }}</b></div>
        <div v-else><b>{{ props.opp.project_id }} {{props.opp.category}}</b> ({{ getCategory(props.opp.category) }})</div>
        <div v-html="props.opp.body"></div>
        <div v-if="opp.just_show_up" class="green">No need to register. Just show up!</div>
        <a v-if="opp.link" :href="opp.link" target="_blank"><div class="button">{{ ['AT', 'EV'].includes(opp.category) ? 'More Information' : 'VOLUNTEER' }}</div></a>
      </div>
    </div>
  </div>
</template>

<style scoped>
  .modal-container {
    display: block; /* Hidden by default */
    position: fixed; /* Stay in place */
    z-index: 1; /* Sit on top */
    padding-top: 100px; /* Location of the box */
    left: 0;
    top: 0;
    width: 100%; /* Full width */
    height: 100%; /* Full height */
    overflow: auto; /* Enable scroll if needed */
    background-color: rgb(0,0,0); /* Fallback color */
    background-color: rgba(0,0,0,0.5); /* Black w/ opacity */
  }

  /* Modal Content */
  .modal {
    margin: auto;
    padding: 20px;
    border-radius: 5px;
    width: 80%;
  }

  /* The Close Button */
  .close {
    color: #aaaaaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
  }

  .close:hover,
  .close:focus {
    color: #000;
    text-decoration: none;
    cursor: pointer;
  }
</style>
