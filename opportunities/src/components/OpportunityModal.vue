<script setup>
import { ref, computed } from 'vue'

import { getCategory, formatModalDateDisplay } from '../utils.js'

const props = defineProps({
  opp: Object
})

const emit = defineEmits(['closeModal'])
</script>

<template>
  <div class="modal-container">
    <div class="modal-content modal">
      <span class="close" @click="emit('closeModal')">&times;</span>
      <div class="opp-wrapper">
        <h2>{{ props.opp.title }}</h2>
        <br/>
        <div><span style="font-weight:bold;">When:</span> {{ formatModalDateDisplay(opp) }}</div>
        <div><span style="font-weight:bold;">Where:</span> {{ props.opp.anywhere ? 'Anywhere' : props.opp.location }}</div>
        <div v-if="props.opp.city">{{ props.opp.city === "Other" ? '' : props.opp.city }}</div>
        <div><span style="font-weight:bold;">VMS Code: </span> 
        <span v-if="props.opp.category === 'AT'"><b>AT: {{ props.opp.project_id }}</b></span>
        <span v-else><b>{{ props.opp.project_id }} {{props.opp.category}}</b> ({{ getCategory(props.opp.category) }})</span></div>
        <br/>
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
    padding-top: 100px; /* Location of the box */
    left: 0;
    top: 0;
    width: 100%; /* Full width */
    height: 100%; /* Full height */
    overflow: auto; /* Enable scroll if needed */
    background-color: rgb(0,0,0); /* Fallback color */
    background-color: rgba(0,0,0,0.5); /* Black w/ opacity */
  }

  .modal-content {
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
