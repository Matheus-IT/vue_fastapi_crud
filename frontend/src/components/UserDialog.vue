<template>
    <v-dialog v-model="modelValue" max-width="600">
      <v-card>
        <v-card-title>{{ mode === 'create' ? 'Create User' : 'Edit User' }}</v-card-title>
        <v-card-text>
          <v-form @submit.prevent="submit">
            <v-text-field v-model="formData.username" label="Username" required />
            <v-text-field v-model="formData.password" label="Password" type="password" />
            
            <v-select
              v-model="formData.roles"
              :items="availableRoles"
              label="Roles"
              multiple
              chips
            />
  
            <v-text-field v-model="formData.preferences.timezone" label="Timezone" />
            
            <v-switch v-model="formData.active" label="Active" />
  
            <v-btn type="submit" color="primary">{{ mode === 'create' ? 'Create' : 'Update' }}</v-btn>
            <v-btn @click="$emit('update:modelValue', false)">Cancel</v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </v-dialog>
  </template>
  
  <script setup>
  import { ref, watch } from 'vue'
  
  const props = defineProps({
    modelValue: Boolean,
    user: Object,
    mode: String
  })
  
  const emit = defineEmits(['update:modelValue', 'submit'])
  
  const availableRoles = ['admin', 'manager', 'tester']
  const formData = ref({
    username: '',
    password: '',
    roles: [],
    preferences: { timezone: '' },
    active: true
  })
  
  watch(() => props.user, (newUser) => {
    if (newUser) {
      formData.value = JSON.parse(JSON.stringify(newUser))
    }
  })
  
  const submit = () => {
    emit('submit', formData.value)
    emit('update:modelValue', false)
  }
  </script>