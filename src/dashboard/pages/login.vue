<template>
    <div class="login-container">
      <div class="login-content">
        <p class="login-info">You need to log in to access the content</p>
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
  .login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #cce5ff;
  }
  
  .login-content {
    text-align: center;
    padding: 20px;
  }
  
  .login-info {
    font-size: 18px;
    margin-bottom: 20px;
  }
  
  .login-form {
    text-align: center;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
    background-color: #e6f7ff;
  }
  
  .form-group {
    margin: 10px 0;
  }
  
  button {
    background-color: #007BFF;
    color: #fff;
    border: none;
    border-radius: 5px;
    padding: 10px 20px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  
  .error-message {
    color: red; /* Red color for error message text */
    margin-top: 10px;
  }
  </style>
  