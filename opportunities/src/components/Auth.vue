<script setup>
import { ref } from 'vue'
import { DOMAIN } from '../utils.js'


const props = defineProps({
  endpoint: String,
})


const endpoint = ref(`${DOMAIN}/auth/${props.endpoint}`)

function handleResponse(response) {
  if (response.data.success) {
    success.value = true
    setTimeout(() => router.push('/'), 2000)
  } else {
    err.value = 'Oops! Something went wrong. Please try again.'
    setTimeout(() => {
      err.value = null
    }, 5000);
  }
}
</script>


<template>
  <Vueform
    size="md"
    :endpoint="endpoint"
    :display-errors="false"
  >
      <TextElement
        name="email"
        placeholder="Email"
        :columns="{
          container: 6,
          label: 12,
          wrapper: 12,
        }"
        :rules="[
          'required',
          'max:255',
        ]"
      />
      <TextElement
        name="password"
        input-type="password"
        :rules="[
          'required',
        ]"
        placeholder="Password"
      />
      <ButtonElement
        name="submit"
        :submits="true"
        button-label="Submit"
        :full="true"
        size="lg"
      />
  </Vueform>
</template>
