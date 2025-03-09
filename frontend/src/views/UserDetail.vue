<template>
    <v-container>
        <v-card>
            <v-card-title class="text-h5">User Details</v-card-title>
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
                        <v-list-item-subtitle>{{ user.preferences?.timezone || 'Not specified' }}</v-list-item-subtitle>
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
                        <v-list-item-subtitle>{{ user.created_at }}</v-list-item-subtitle>
                    </v-list-item>

                    <v-list-item>
                        <v-list-item-title>Last Updated</v-list-item-title>
                        <v-list-item-subtitle>{{ user.last_updated }}</v-list-item-subtitle>
                    </v-list-item>
                </v-list>
            </v-card-text>
        </v-card>
    </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { format } from 'date-fns'

const route = useRoute()
const user = ref({
    username: '',
    roles: [],
    preferences: { timezone: 'UTC' }, // Default value
    active: true,
    created_at: '',
    last_updated: ''
})

const fetchUser = async () => {
    try {
        const response = await axios.get(`http://localhost:5000/users/${route.params.username}`)
        console.log('response detail', response);
        
        user.value = response.data
    } catch (error) {
        console.error('Error fetching user:', error)
    }
}

onMounted(() => {
    fetchUser()
})
</script>