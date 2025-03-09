<template>
    <v-container>
        <v-card>
            <v-card-title class="text-h5">Users Management</v-card-title>

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