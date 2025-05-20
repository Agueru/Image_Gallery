<template>
    <div class="container">
        <h1 class="text-center mb-4">Signup</h1>
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <form @submit.prevent="signup">
                            <div class="form-group my-2">
                                <label for="name">Name</label>
                                <input type="text" class="form-control" id="name" placeholder="Enter name"
                                    @change="handleNameChange" required :value="this.name">
                            </div>
                            <div class="form-group my-2">
                                <label for="email">Email address</label>
                                <input type="email" class="form-control" id="email" placeholder="Enter email"
                                    @change="handleEmailChange" required :value="this.email">
                            </div>
                            <div class="form-group my-2">
                                <label for="password">Password</label>
                                <input type="password" class="form-control" id="password" placeholder="Enter password"
                                    @change="handlePasswordChange" required :value="this.password">
                                <div v-if="this.passwordError" class="text-danger">{{ this.passwordError }}</div>
                            </div>
                            <button type="submit" class="btn btn-outline-dark my-3">Signup</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
  
<script>
import axios from 'axios';
import { toast } from 'vue3-toastify';

export default {
    name: 'Signup',
    data() {
        return {
            email: '',
            password: '',
            name: '',
            passwordError: '',
        };
    },
    methods: {
        validatePassword() {
            if (this.password.length < 8) {
                this.passwordError = 'Password must be at least 8 characters long';
            }
            else {
                this.passwordError = '';
            }
        },
        handleEmailChange(event) {
            this.email = event.target.value;
        },
        handlePasswordChange(event) {
            this.password = event.target.value;
        },
        handleNameChange(event) {
            this.name = event.target.value;
        },
        signup() {
            const formData = new FormData();
            formData.append('email', this.email);
            formData.append('password', this.password);
            formData.append('name', this.name);

            this.validatePassword();

            !this.passwordError &&
                axios.post('http://localhost:5000/api/v1/signup', formData)
                    .then((response) => {
                        if (response.status === 201) {
                            toast('User Created, Please Login', {
                                type: 'success',
                            })
                        }
                       
                        this.email = '';
                        this.password = '';
                        this.name = '';
                    })
                    .catch((error) => {
                        if (error.response.status === 400) {
                            Object.keys(error.response.data).forEach((key) => {
                                toast(error.response.data[key], {
                                    type: 'error',
                                })
                            })
                        }
                        else {
                            toast('Something went wrong', {
                                type: 'error',
                            })
                        }
                    });
        },
    },
};
</script>
  