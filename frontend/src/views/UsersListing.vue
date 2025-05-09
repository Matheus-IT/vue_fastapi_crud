<template>
    <v-container>
        <v-card>
            <v-card-title class="d-flex justify-space-between align-center ">
                <span class="text-h5">Users Management</span>
                <v-btn color="primary" @click="openCreateDialog()">
                    <v-icon left>mdi-plus</v-icon>
                    Create User
                </v-btn>
            </v-card-title>

            <UserFormDialog :dialog="showUserDialog" @update:dialog="showUserDialog = $event" :isEdit="isEditMode"
                :userData="selectedUser" @submit="handleFormSubmit" />

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
                    {{ formatDateTime(item.created_at) }}
                </template>
                
                <template v-slot:item.last_updated="{ item }">
                    {{ formatDateTime(item.last_updated) }}
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
import UserFormDialog from '@/components/UserFormDialog.vue'

const host = 'http://localhost:8000';

const formatDateTime = (dateTimeString) => {
  const date = new Date(dateTimeString);
  return date.toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: true, // Use 12-hour format (AM/PM)
  });
};

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
const showUserDialog = ref(false)
const isEditMode = ref(false)
const selectedUser = ref(null)

const openCreateDialog = () => {
    console.log('Opening create dialog')
    isEditMode.value = false
    selectedUser.value = null
    showUserDialog.value = true
}

const editUser = (user) => {
    const confirmEdit = confirm(`Are you sure you want to edit ${user.username}?`)
    if (!confirmEdit) return

    console.log('Opening edit dialog for user:', user)
    isEditMode.value = true
    selectedUser.value = { ...user }
    showUserDialog.value = true
}

const handleFormSubmit = async (formData) => {
    try {
        // Remove the _id field from the formData
        const { _id, ...payload } = formData

        if (isEditMode.value) {
            console.log('Updating user:', formData)
            await axios.put(`${host}/users/${selectedUser.value._id}`, payload)
        } else {
            console.log('Creating user:', payload)
            await axios.post(`${host}/users`, payload)
        }
        showUserDialog.value = false
        await fetchUsers() // Refresh the list
    } catch (error) {
        console.error('Error saving user:', error)
        alert(`Error saving user: ${error.response?.data?.error || error.message}`)
    }
}

const fetchUsers = async () => {
    try {
        const response = await axios.get(`${host}/users`)
        users.value = response.data
    } catch (error) {
        console.error('Error fetching users:', error)
    } finally {
        loading.value = false
    }
}

const deleteUser = async (user) => {
    const confirmDelete = confirm(`Are you sure you want to delete ${user.username}?`)
    if (!confirmDelete) return

    try {
        await axios.delete(`${host}/users/${user._id}`)
        users.value = users.value.filter(u => u._id !== user._id)
        alert('User deleted successfully')
    } catch (error) {
        console.error('Error deleting user:', error)
        alert(`Error deleting user: ${error.response?.data?.error || error.message}`)
        await fetchUsers()
    }
}

onMounted(() => {
    fetchUsers()
})
</script>