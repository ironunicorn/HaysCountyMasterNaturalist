import './assets/main.css'

import { createApp } from 'vue'
import Vueform from '@vueform/vueform'
import vueformConfig from './../vueform.config'
import { createWebHistory, createRouter } from 'vue-router'
import App from './App.vue'
import Opportunities from './components/Opportunities.vue'
import OpportunityForm from './components/OpportunityForm.vue'


const routes = [
  { path: '/', component: Opportunities },
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
