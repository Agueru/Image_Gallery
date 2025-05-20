<template>
    <div class="position-absolute top-0 end-0 my-2 me-2">
        <div v-if="$store.state.isAuthenticated">
            <button class="btn btn-outline-danger" @click="logout">Logout</button>
        </div>
        <div v-else>
            <RouterLink to="/login">
                <button class="btn btn-dark me-2">Login</button>
            </RouterLink>
            <RouterLink to="/signup">
                <button class="btn btn-dark">Signup</button>
            </RouterLink>
        </div>
    </div>
    <div class="position-absolute top-0 start-0 my-2 ms-2 d-flex">
        <RouterLink to="/">
            <button class="btn mx-2 btn-dark">Home</button>
        </RouterLink>
        <div v-if="$store.state.isAuthenticated">
            <RouterLink to="upload-image">
                <button class="btn btn-dark">Upload Image</button>
            </RouterLink>
        </div>
    </div>
</template>

<script>
import { RouterLink } from 'vue-router';
import { toast } from 'vue3-toastify';
import axios from 'axios';

export default {
    name: 'ButtonsBar',
    methods: {
        handleLogout() {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            this.$store.commit('setUserLoggedOut');
            this.$router.push('/login');
            toast('Logged Out', {
                type: 'success',
            });
        },
        logout() {
            const token = localStorage.getItem('token');
            axios.post('http://localhost:5000/api/v1/logout', {}, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }).then(response => {
                if (response.status === 200) {
                    this.handleLogout()
                }
            }).catch(error => {
                if (error.response.status === 401) {
                    this.handleLogout()
                }
            })

        },
    },
};

</script>