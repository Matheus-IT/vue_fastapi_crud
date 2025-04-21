<template>
    <v-dialog :model-value="dialog" @update:model-value="$emit('update:dialog', $event)" max-width="600" persistent>
        <v-card>
            <v-card-title class="text-h5">
                {{ isEdit ? 'Edit User' : 'Create User' }}
            </v-card-title>
            <v-card-text>
                <v-form ref="form" @submit.prevent="handleSubmit">
                    <v-text-field v-model="formData.username" label="Username" :rules="[required]" :disabled="isEdit"
                        required></v-text-field>

                    <v-text-field v-if="!isEdit" v-model="formData.password" label="Password" type="password"
                        :rules="[required, passwordStrength]" required></v-text-field>

                    <v-select v-model="formData.preferences.timezone" :items="timezones" label="Timezone"
                        :rules="[required]" required></v-select>

                    <v-checkbox v-model="formData.roles" label="Admin" value="admin"></v-checkbox>

                    <v-checkbox v-model="formData.roles" label="Manager" value="manager"></v-checkbox>

                    <v-checkbox v-model="formData.roles" label="Tester" value="tester"></v-checkbox>

                    <v-switch v-model="formData.active" label="Active" color="success" inset></v-switch>

                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="error" @click="closeDialog">
                            Cancel
                        </v-btn>
                        <v-btn color="primary" type="submit">
                            {{ isEdit ? 'Save Changes' : 'Create' }}
                        </v-btn>
                    </v-card-actions>
                </v-form>
            </v-card-text>
        </v-card>
    </v-dialog>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
    dialog: Boolean,
    isEdit: Boolean,
    userData: Object
})

const emit = defineEmits(['submit', 'update:dialog'])

const form = ref(null)
const formData = ref({
    username: '',
    password: '',
    roles: [],
    preferences: {
        timezone: ''
    },
    active: true
})

const timezones = ref([
    'America/New_York',
    'Europe/London',
    'Asia/Tokyo',
    'Europe/Paris',
    'Australia/Sydney'
])

const required = (value) => !!value || 'This field is required'
const passwordStrength = (value) =>
    (value && value.length >= 8) || 'Password must be at least 8 characters'

// Watch for changes in userData (for edit mode)
watch(
    () => props.userData,
    (newData) => {
        if (newData) {
            formData.value = { ...newData }
        }
    },
    { immediate: true }
)

const handleSubmit = async () => {
    const { valid } = await form.value.validate()
    if (!valid) return

    emit('submit', formData.value)
}

const closeDialog = () => {
    form.value.reset()
    emit('update:dialog', false)
}
</script>