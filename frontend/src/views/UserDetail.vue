<template>
    <v-container>
        <v-card>
            <v-card-title class="d-flex justify-space-between align-center">
                <div>
                    <v-btn icon @click="goBack" class="mr-2">
                        <v-icon>mdi-arrow-left</v-icon>
                    </v-btn>
                    <span class="text-h5">User Details</span>
                </div>
                <div>
                    <v-btn color="primary" @click="openEditDialog(user)" class="mr-2">
                        <v-icon left>mdi-pencil</v-icon>
                        Edit
                    </v-btn>
                    <v-btn color="error" @click="deleteUser">
                        <v-icon left>mdi-delete</v-icon>
                        Delete
                    </v-btn>
                </div>
            </v-card-title>

            <!-- Reusable Edit Dialog -->
            <UserFormDialog :dialog="showEditDialog" @update:dialog="showEditDialog = $event" :isEdit="true"
                :userData="user" @submit="handleEditSubmit" />

            <v-card-text>
                <v-list>
                    <v-list-item>
                        <v-list-item-title>Username</v-list-item-title>
                        <v-list-item-subtitle>{{ user.username }}</v-list-item-subtitle>
                    </v-list-item>

                    <v-list-item>
                        <v-list-item-title>Roles</v-list-item-title>
                        <v-list-item-subtitle>
                            <v-chip v-for="role in user.roles" :key="role" class="ma-1" color="primary" size="small">
                                {{ role }}
                            </v-chip>
                        </v-list-item-subtitle>
                    </v-list-item>

                    <v-list-item>
                        <v-list-item-title>Timezone</v-list-item-title>
                        <v-list-item-subtitle>{{ user.preferences.timezone }}</v-list-item-subtitle>
                    </v-list-item>

                    <v-list-item>
                        <v-list-item-title>Is Active?</v-list-item-title>
                        <v-list-item-subtitle>
                            <v-icon :color="user.active ? 'success' : 'error'">
                                {{ user.active ? 'mdi-check-circle' : 'mdi-close-circle' }}
                            </v-icon>
                        </v-list-item-subtitle>
                    </v-list-item>

                    <v-list-item>
                        <v-list-item-title>Created At</v-list-item-title>
                        <v-list-item-subtitle>{{ formatDate(user.created_at) }}</v-list-item-subtitle>
                    </v-list-item>

                    <v-list-item>
                        <v-list-item-title>Last Updated</v-list-item-title>
                        <v-list-item-subtitle>{{ formatDate(user.last_updated) }}</v-list-item-subtitle>
                    </v-list-item>
                </v-list>
            </v-card-text>
        </v-card>
    </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import UserFormDialog from '@/components/UserFormDialog.vue'

const route = useRoute()
const router = useRouter()
const user = ref({
    username: '',
    roles: [],
    preferences: { timezone: 'UTC' }, // Default value
    active: true,
    created_at: '',
    last_updated: ''
})
const showEditDialog = ref(false)

const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString()
}

const fetchUser = async () => {
    try {
        const response = await axios.get(`http://localhost:5000/users/${route.params.user_id}`)
        console.log('response', response);

        user.value = response.data
    } catch (error) {
        console.error('Error fetching user:', error)
        alert(`Error fetching user: ${error.response?.data?.error || error.message}`)
    }
}

const openEditDialog = (user) => {
    const confirmEdit = confirm(`Are you sure you want to edit ${user.username}?`)
    if (!confirmEdit) return

    showEditDialog.value = true
}

const handleEditSubmit = async (formData) => {
    try {
        // Remove the _id field from the formData
        const { _id, ...updateData } = formData

        await axios.put(`http://localhost:5000/users/${route.params.user_id}`, updateData)
        showEditDialog.value = false
        await fetchUser() // Refresh the user data
    } catch (error) {
        console.error('Error updating user:', error)
        alert(`Error updating user: ${error.response?.data?.error || error.message}`)
    }
}

const deleteUser = async () => {
    const confirmDelete = confirm(`Are you sure you want to delete ${user.value.username}?`)
    if (!confirmDelete) return

    try {
        await axios.delete(`http://localhost:5000/users/${route.params.user_id}`)
        alert('User deleted successfully')
        router.push({ name: 'users' }) // Redirect to the users listing page
    } catch (error) {
        console.error('Error deleting user:', error)
        alert(`Error deleting user: ${error.response?.data?.error || error.message}`)
    }
}

const goBack = () => {
    router.go(-1) // Go back to the previous page
}

onMounted(() => {
    fetchUser()
})
</script>