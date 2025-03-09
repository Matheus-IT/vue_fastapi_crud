<template>
    <v-container>
        <v-card>
            <v-card-title class="d-flex justify-space-between align-center">
                <span class="text-h5">Users Management</span>
                <v-btn color="primary" @click="showCreateDialog = true">
                    <v-icon left>mdi-plus</v-icon>
                    Create User
                </v-btn>
            </v-card-title>

            <v-dialog v-model="showCreateDialog" max-width="600">
                <v-card>
                    <v-card-title class="text-h5">Create New User</v-card-title>
                    <v-card-text>
                        <v-form ref="createForm" @submit.prevent="handleCreateUser">
                            <v-text-field v-model="newUser.username" label="Username" :rules="[required]"
                                required></v-text-field>

                            <v-text-field v-model="newUser.password" label="Password" type="password"
                                :rules="[required, passwordStrength]" required></v-text-field>

                            <v-select v-model="newUser.preferences.timezone" :items="timezones" label="Timezone"
                                :rules="[required]" required></v-select>

                            <v-checkbox v-model="newUser.roles" label="Admin" value="admin"></v-checkbox>

                            <v-checkbox v-model="newUser.roles" label="Manager" value="manager"></v-checkbox>

                            <v-checkbox v-model="newUser.roles" label="Tester" value="tester"></v-checkbox>

                            <v-switch v-model="newUser.active" label="Active" color="success" inset></v-switch>

                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn color="error" @click="showCreateDialog = false">
                                    Cancel
                                </v-btn>
                                <v-btn color="primary" type="submit">
                                    Create
                                </v-btn>
                            </v-card-actions>
                        </v-form>
                    </v-card-text>
                </v-card>
            </v-dialog>

            <v-data-table :headers="headers" :items="users" :loading="loading" loading-text="Loading users...">
                <template v-slot:item.username="{ item }">
                    <router-link :to="`/users/${item._id}`" class="text-decoration-none text-primary">
                        {{ item.username }}
                    </router-link>
                </template>

                <template v-slot:item.roles="{ item }">
                    <v-chip v-for="role in item.roles" :key="role" class="ma-1" color="primary" size="small">
                        {{ role }}
                    </v-chip>
                </template>

                <template v-slot:item.preferences.timezone="{ item }">
                    {{ item.preferences.timezone }}
                </template>

                <template v-slot:item.active="{ item }">
                    <v-icon :color="item.active ? 'success' : 'error'">
                        {{ item.active ? 'mdi-check-circle' : 'mdi-close-circle' }}
                    </v-icon>
                </template>

                <template v-slot:item.created_at="{ item }">
                    {{ item.created_at }}
                </template>

                <template v-slot:item.actions="{ item }">
                    <v-btn icon variant="text" @click="editUser(item)">
                        <v-icon color="primary">mdi-pencil</v-icon>
                    </v-btn>
                    <v-btn icon variant="text" @click="deleteUser(item)">
                        <v-icon color="error">mdi-delete</v-icon>
                    </v-btn>
                </template>
            </v-data-table>
        </v-card>
    </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { format } from 'date-fns'

const headers = ref([
    { title: 'Username', key: 'username' },
    { title: 'Roles', key: 'roles' },
    { title: 'Timezone', key: 'preferences.timezone' },
    { title: 'Is Active?', key: 'active' },
    { title: 'Created At', key: 'created_at' },
    { title: 'Last Updated', key: 'last_updated' },
    { title: 'Actions', key: 'actions', sortable: false }
])

const users = ref([])
const loading = ref(true)
const showCreateDialog = ref(false)
const createForm = ref(null)

const timezones = ref([
    'America/New_York',
    'Europe/London',
    'Asia/Tokyo',
    'Europe/Paris',
    'Australia/Sydney'
])

const newUser = ref({
    username: '',
    password: '',
    roles: [],
    preferences: {
        timezone: ''
    },
    active: true
})

const required = (value) => !!value || 'This field is required'

const passwordStrength = (value) =>
    (value && value.length >= 8) || 'Password must be at least 8 characters'

const fetchUsers = async () => {
    try {
        const response = await axios.get('http://localhost:5000/users')
        console.log('response', response)
        users.value = response.data
    } catch (error) {
        console.error('Error fetching users:', error)
    } finally {
        loading.value = false
    }
}

const handleCreateUser = async () => {
    const { valid } = await createForm.value.validate()
    if (!valid) return

    try {
        const res = await axios.post('http://localhost:5000/users', newUser.value)
        console.log('res created', res);
        showCreateDialog.value = false
        newUser.value = {
            username: '',
            password: '',
            roles: [],
            preferences: { timezone: '' },
            active: true
        }
        await fetchUsers() // Refresh the list
    } catch (error) {
        console.error('Error creating user:', error)
        alert('Error creating user: ' + error.response?.data?.error || error.message)
    }
}

const editUser = (user) => {
    console.log('Edit user:', user)
}

const deleteUser = (user) => {
    console.log('Delete user:', user)
}

onMounted(() => {
    fetchUsers()
})
</script>