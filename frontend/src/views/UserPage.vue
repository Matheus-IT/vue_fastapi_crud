<template>
    <v-container>
        <v-card>
            <v-card-title>
                {{ user.username }}'s Details
            </v-card-title>
            <v-card-text>
                <p><strong>Username:</strong> {{ user.username }}</p>
                <p><strong>Roles:</strong> {{ user.roles.join(', ') }}</p>
                <p><strong>Timezone:</strong> {{ user.preferences?.timezone }}</p>
                <p><strong>Active:</strong> {{ user.active ? 'Yes' : 'No' }}</p>
                <p><strong>Last Updated:</strong> {{ user.last_updated_ts }}</p>
                <p><strong>Created At:</strong> {{ user.created_ts }}</p>
            </v-card-text>
            <v-card-actions>
                <v-btn color="primary" @click="editUser()">Edit</v-btn>
                <v-btn color="red" @click="confirmDelete()">Delete</v-btn>
            </v-card-actions>
        </v-card>

        <!-- Reuse the dialog component for editing -->
        <user-dialog :dialog="dialog" :edited-user="user" @close="closeDialog" @save="saveUser" />

        <!-- Delete confirmation dialog -->
        <v-dialog v-model="deleteDialog" max-width="500">
            <v-card>
                <v-card-title class="headline">Confirm Delete</v-card-title>
                <v-card-text>
                    Are you sure you want to delete <strong>{{ user.username }}</strong>?
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn text @click="deleteDialog = false">Cancel</v-btn>
                    <v-btn color="red" text @click="deleteUser()">Delete</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-container>
</template>

<script>
import axios from 'axios'
import UserDialog from '@/components/UserDialog.vue'

export default {
    name: "UserPage",
    components: { UserDialog },
    props: ['id'],
    data() {
        return {
            user: {},
            dialog: false,
            deleteDialog: false
        }
    },
    created() {
        this.fetchUser()
    },
    methods: {
        fetchUser() {
            axios.get(`http://localhost:5000/users/${this.id}`)
                .then(response => {
                    this.user = response.data
                })
        },
        editUser() {
            this.dialog = true
        },
        closeDialog() {
            this.dialog = false
            this.fetchUser()
        },
        saveUser(updatedUser) {
            axios.put(`http://localhost:5000/users/${this.user._id}`, updatedUser)
                .then(() => this.closeDialog())
        },
        confirmDelete() {
            this.deleteDialog = true
        },
        deleteUser() {
            axios.delete(`http://localhost:5000/users/${this.user._id}`)
                .then(() => {
                    this.deleteDialog = false
                    this.$router.push({ name: "MainPage" })
                })
        }
    }
}
</script>