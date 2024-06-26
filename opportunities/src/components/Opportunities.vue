<script setup>
import axios from 'axios'
import moment from 'moment'
import { ref, watch } from 'vue'

import Day from './Day.vue'
import OpportunityModal from './OpportunityModal.vue'
import { getCategory, DOMAIN } from '../utils.js'


const ANY_TIME = 'Any Time'
const opportunities = ref([])
const categories = ref(new Set())
const cities = ref(new Set())
const searchTitleAndBody = ref(null)
const selectedCategories = ref(new Set())
const selectedCities = ref(new Set())
const showExpired = ref(false)
const filteredOpportunities = ref({})
const user = ref({})
const days = ref([])
const openOpp = ref({})


function addRemoveCategory(e, category) {
  selectedCategories.value.has(category) ?
    selectedCategories.value.delete(category) :
    selectedCategories.value.add(category)

  // vue doesn't know when sets are updated
  selectedCategories.value = new Set(selectedCategories.value)
}

function addRemoveCity(e, city) {
  selectedCities.value.has(city) ?
    selectedCities.value.delete(city) :
    selectedCities.value.add(city)

  // vue doesn't know when sets are updated
  selectedCities.value = new Set(selectedCities.value)
}

function orderByDate(opps) {
  opps.sort((a, b) => {
    let aTime = a.event_start ? moment(a.event_start) : moment()
    let bTime = b.event_start ? moment(b.event_start) : moment()

    return aTime > bTime ? 1 : -1
  })
}

function removeExpired(opps) {
  return opps.filter((opp) => {
    let expirationDate;
    if (opp.expiration_date && opp.event_start) {
      expirationDate = (
        moment(opp.expiration_date) >= moment(opp.event_start) ?
        opp.event_start :
        opp.expiration_date
      )
    } else {
      expirationDate = opp.expiration_date || opp.event_start
    }

    return !expirationDate || (moment() <= moment(expirationDate))
  })
}

function getReadableDate(day) {
  return day.format('LLLL').replace(' '.concat(day.format('LT')), '').slice(0, -6)
}

function groupByDay(opps) {
  const opportunitiesByDay = {}
  opps.forEach((opp) => {
    let day;
    if (opp.event_start) {
      let fullDay = moment(opp.event_start)
      day = getReadableDate(fullDay)
    } else {
      day = ANY_TIME
    }
    if (day in opportunitiesByDay) {
      opportunitiesByDay[day].push(opp)
    } else {
      opportunitiesByDay[day] = [opp]
    }
  })
  return opportunitiesByDay
}

function getAllDays() {
  let day = moment()
  day = day.subtract(45, 'days')
  for (let i = 0; i < 135; i++) {
    if (i === 45) days.value.push(ANY_TIME)
    days.value.push(getReadableDate(day))
    day = day.add(1, 'days')
  }
}

function filterOpportunities() {
  let newOpps = [...opportunities.value]
  if (!showExpired.value) {
    newOpps = removeExpired(newOpps)
  }
  if (searchTitleAndBody.value) {
    newOpps = newOpps.filter((opp) => {
      return opp.title.toLowerCase().includes(searchTitleAndBody.value.toLowerCase()) ||
        opp.body.toLowerCase().includes(searchTitleAndBody.value.toLowerCase())
    })
  }
  if (selectedCities.value.size) {
    newOpps = newOpps.filter((opp) => selectedCities.value.has(opp.anywhere ? 'Anywhere' : opp.city))
  }
  if (selectedCategories.value.size) {
    newOpps = newOpps.filter((opp) => selectedCategories.value.has(getCategory(opp.category)))
  }
  groupByDay(newOpps)
  filteredOpportunities.value = groupByDay(newOpps)
}

function openModal(opp) {
  openOpp.value = opp
}

async function fetchOpportunities() {
  const res = await axios.get(DOMAIN.concat(`/api/opportunities`))
  opportunities.value = await res.data

  cities.value = new Set(opportunities.value.map((opp) => opp.city || 'Anywhere'))
  categories.value = new Set(opportunities.value.map((opp) => getCategory(opp.category)))
  orderByDate(opportunities.value)
  filterOpportunities()
  getAllDays()
}

async function fetchUser() {
  const res = await axios.get(DOMAIN.concat(`/auth/user`))
  user.value = await res.data
}

watch(searchTitleAndBody, filterOpportunities)
watch(selectedCities, filterOpportunities)
watch(selectedCategories, filterOpportunities)
watch(showExpired, filterOpportunities)

fetchOpportunities()
fetchUser()
</script>

<template>
  <div class="user">
    <div v-if="user.id">
      <RouterLink v-if="user.admin || user.project_coordinator" to="/new">Create Opportunity</RouterLink>
      <a v-else href="https://docs.google.com/forms/d/e/1FAIpQLSf0j6GQVsDAo0UZswqfXhGRk7l5HcoEhqOvnsmudf5KhiDLrA/viewform?usp=sf_link">Request Editing Access</a>
      <span> | </span>
      <a href="/auth/logout">Logout</a>
    </div>
    <div v-else>
      Project Coordinators:
      <RouterLink to="/signup">Sign Up</RouterLink> |
      <a href="/login">Log in</a>
    </div>
  </div>
  <div class="everything">
    <div class="filters">
      <div class="filter">
        <label><h3>Search </h3></label>
        <input v-model="searchTitleAndBody">
        <br>
        <br>
        <label>
          <input type="checkbox" v-model="showExpired">
          Show expired opportunities
        </label>
      </div>
      <div class="filter">
        <h3>Categories</h3>
        <div v-for="category in categories">
          <label>
            <input
                type="checkbox"
                @change="addRemoveCategory(e, category)"
                :value="category"/>
            {{ category }}
          </label>
        </div>
      </div>
      <div class="filter">
        <h3>Cities</h3>
        <div v-for="city in cities">
          <label>
            <input
                type="checkbox"
                @change="addRemoveCity(e, city)"
                :value="city"/>
            {{ city }}
          </label>
        </div>
      </div>
    </div>
    <div class="weeks">
      <div class="day" v-if="showExpired" v-for="day in days">
        <div class="day-header">
          {{ day }}
        </div>
        <Day
          :admin="user.admin"
          :userId="user.id"
          :opps="filteredOpportunities[day] || []"
          @modalOpp="openModal"
        />
      </div>
      <div class="day" v-else v-for="day in days.slice(45)">
        <div class="day-header">
          {{ day }}
        </div>
        <Day
          :admin="user.admin"
          :userId="user.id"
          :opps="filteredOpportunities[day] || []"
          @modalOpp="openModal"
        />
      </div>
    </div>
  </div>
  <OpportunityModal :opp="openOpp" />
</template>

<style scoped>
  .user {
    text-align: right;
  }
  .filters  {
    line-height: 1.5;
    margin-right: 10px;
  }
  .filter {
    margin: 20px;
  }

  .day-header {
    padding: 5px;
  }

  @media (min-width: 1024px) {
    .weeks {
      display: flex;
      flex-wrap: wrap;
    }
    .day {
      flex-grow: 1;
      width: 14%;
    }
    .opp-list {
      max-width: 720px;
    }
    .filters  {
      display: flex;
    }
  }
</style>
