<template>
  <div class="container">
    <h1 class="text-center mb-4">Login</h1>
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-body">
            <form @submit.prevent="login">
              <div class="form-group my-2">
                <label for="email">Email address</label>
                <input type="email" class="form-control" id="email" placeholder="Enter email" @change="handleEmailChange">
              </div>
              <div class="form-group my-2">
                <label for="password">Password</label>
                <input type="password" class="form-control" id="password" placeholder="Enter password"
                  @change="handlePasswordChange">
              </div>
              <button type="submit" class="btn btn-outline-dark my-3">Login</button>
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

  name: 'Login',
  data() {
    return {
      email: '',
      password: '',
    };
  },
  methods: {
    handleEmailChange(event) {
      this.email = event.target.value;
    },
    handlePasswordChange(event) {
      this.password = event.target.value;
    },
    login() {
      const formData = new FormData();
      formData.append('email', this.email);
      formData.append('password', this.password);

      axios.post('http://localhost:5000/api/v1/login', formData)
        .then((response) => {
          if (response.status === 200) {
            const token = response.data.access_token;
            localStorage.setItem('token', token);
            localStorage.setItem("user", JSON.stringify(response.data))
            this.$store.commit("setUserLoggedIn", response.data)
            toast('Logged In', {
              type: 'success',
            })
            this.$router.push("/");
          }
          
          this.email = '';
          this.password = '';
        })
        .catch((error) => {
          if (error.response.status === 400) {
            Object.keys(error.response.data).forEach((key) => {
              toast(error.response.data[key], {
                type: 'error',
              })
            })
          }else if(error.response.status === 404){
            toast(error.response.data.error, {
              type: 'error',
            })
          }
        });
    },
  },
};

</script>
  