<template>
  <div class="login-content">
      <form @submit.prevent="login" class="login-form">
          <div class="form-group">
              <label for="username">Username:</label>
              <input type="text" id="username" v-model="formData.username" />
          </div>
          <div class="form-group">
              <label for="password">Password:</label>
              <input type="password" id="password" v-model="formData.password" />
          </div>
          <button type="submit">Login</button>
      </form>
      <p class="error-message" v-if="showErrorMessage">{{ errorMessage }}</p>
  </div>
</template>
  
<script lang="ts">
  import { Component, Vue } from 'nuxt-property-decorator';
  import axios from 'axios';
  
  @Component
  export default class LoginPage extends Vue {
    formData: { username: string; password: string } = {
      username: '',
      password: ''
    };
    showErrorMessage: boolean = false;
    errorMessage: string = '';
  
    async login() {
      try {
        const response = await axios.post('http://localhost:8000/api/v1/login', this.formData);
        const token = response.data.access_token;

        // Save the token to localStorage
        localStorage.setItem('token', token);

        // Redirect to the books page after successful login
        this.$router.push('/books');
      } catch (error: any) {
        console.error('Login error:', error);
        if (error.response && error.response.status === 400) {
          this.showErrorMessage = true;
          this.errorMessage = 'Incorrect username or password';
        }
      }
    }
  }
</script>
  
<style scoped lang="scss">
  @import "./style.css";
</style>
  