<script setup>
import axios from 'axios'
import { ref } from 'vue'

import { DOMAIN } from '../utils.js'

const users = ref([])

async function fetchUsers() {
  const res = await axios.get(DOMAIN.concat(`/api/users`))
  users.value = await res.data
}

fetchUsers()

</script>

<template>
  <div class="navigation">
    <RouterLink to="/">Home</RouterLink>
  </div>
  <h1>Users</h1>
  <div v-for="user in users">
    <br/>
    <h2 class="user-email">{{ user.email }}</h2> 
    Admin <input
      type="checkbox"
      id="admin: {{ user.id }}"
      value="{{ user.admin === 1 }}" />
    <br/>
    Project Coordinator <input
      type="checkbox"
      id="project_coordinator: {{ user.id }}"
      value="{{ user.project_coordinator === 1 }}" />
  </div>
</template>

<style media="screen">
  .navigation {
    text-align: right;
  }
</style>
