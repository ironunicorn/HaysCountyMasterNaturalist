import './assets/main.css'

import { createApp } from 'vue'
import Vueform from '@vueform/vueform'
import vueformConfig from './../vueform.config'
import { createWebHistory, createRouter } from 'vue-router'
import App from './App.vue'
import axios from 'axios'

import Opportunities from './components/Opportunities.vue'
import OpportunityForm from './components/OpportunityForm.vue'
import Auth from './components/Auth.vue'


axios.defaults.withCredentials = true
axios.interceptors.response.use(function (response) {
  axios.defaults.headers.common['X-CSRFToken'] = response.headers['csrf-token']
  console.log(response.headers['csrf-token'])

  return response
})

const routes = [
  { path: '/', component: Opportunities },
  { path: '/signup', component: Auth, props: { endpoint: 'signup'} },
  { path: '/login', component: Auth, props: { endpoint: 'login'} },
  { path: '/new', component: OpportunityForm, props: {id: ''} },
  { path: '/:id', component: OpportunityForm, props: true },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

const app = createApp(App)

app.use(Vueform, vueformConfig)
app.use(router)
app.mount('#app')
