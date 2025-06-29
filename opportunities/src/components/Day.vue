<script setup>
import { ref, computed } from 'vue'

import { getCategory, formatDateDisplay } from '../utils.js'


const props = defineProps({
  opps: Array,
  userId: Number,
  admin: Boolean,
})

const emit = defineEmits(['modalOpp'])


function isEditor(admin, userId, opp) {
  return admin || opp.owner === userId
}

function openModal(opp) {
  emit('modalOpp', opp)
}

</script>

<template>
  <div class="opp-list">
    <div class="opp-wrapper" v-for="opp in opps" @click="openModal(opp)">
      <div v-if="isEditor(admin, userId, opp)" style="text-align: right;">
        <RouterLink class="hover-show vf-btn vf-btn-primary" :to="`/${opp.id}`">Edit</RouterLink>
      </div>
      <h2>{{ opp.title }}</h2>
      <div style="font-weight:bold;">{{ formatDateDisplay(opp) }}</div>
      <div><i>{{ opp.anywhere ? 'Anywhere' : opp.location }}</i></div>
      <div v-if="opp.city"><i>{{ opp.city }}</i></div>
      <div v-if="opp.category === 'AT'"><b>AT: {{ opp.project_id }}</b></div>
      <div v-else-if="opp.category === 'EV'"><b>{{ opp.project_id }}</b></div>
      <div v-else><b>{{ opp.project_id }} {{opp.category}}</b> ({{ getCategory(opp.category) }})</div>
      <div v-if="opp.just_show_up" class="green">No need to register. Just show up!</div>
      <a v-if="opp.link" :href="opp.link" target="_blank"><div class="button">{{ ['AT', 'EV'].includes(opp.category) ? 'More Information' : 'VOLUNTEER' }}</div></a>
    </div>
  </div>
</template>

<style scoped>
  .opp-wrapper {
    margin: 5px;
    padding: 5px;
    border: 1px solid grey;
    border-radius: 5px;
    font-size: .85em;
    cursor: pointer;
  }
  .hover-show {
    display:none;
  }
  .opp-wrapper:hover .hover-show {
    display: block;
    position: absolute;
  }

  h2 {
    font-size: 1.25em;
  }

  @media (min-width: 1200px) {
    .everything {
      display: flex;
    }
    .opp-list {
      max-width: 1500px;
    }
  }
</style>
