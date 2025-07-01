<script setup>
import axios from 'axios'
import { ref } from 'vue'

import { DOMAIN } from '../utils.js'

const users = ref([])
const working = ref(false)

async function fetchUsers() {
  const res = await axios.get(DOMAIN.concat(`/api/users`))
  users.value = await res.data
}

async function updateUser(user, privilege) {
  working.value = true
  user[privilege] = user[privilege] === 1 ? 0 : 1
  const res = await axios.post(DOMAIN.concat(`/api/users/${user.id}`), {
    admin: user.admin === 1, 
    project_coordinator: user.project_coordinator === 1,
  }, {
    headers: {
      'Content-Type': 'application/json'
    }
  })
  let success = await res.data
  working.value = false
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
      :checked="user.admin"
      :disabled="working"
      @change="updateUser(user, 'admin')" />
    <br/>
    Project Coordinator <input
      type="checkbox"
      :checked="user.project_coordinator" 
      :disabled="working"
      @change="updateUser(user, 'project_coordinator')"/>
  </div>
</template>

<style media="screen">
  .navigation {
    text-align: right;
  }
</style>
