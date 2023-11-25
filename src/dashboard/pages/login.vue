<template>
    <div class="auth-container">
      <div class="slider">
        <button class="slide-button" @click="isLogin = true" :class="{ active: isLogin }">Login</button>
        <button class="slide-button" @click="isLogin = false" :class="{ active: !isLogin }">Register</button>
        <div class="slider-background" :style="{ 'transform': isLogin ? 'translateX(0)' : 'translateX(100%)' }"></div>
      </div>
      <div v-if="isLogin">
        <LoginPage />
      </div>
      <div v-else>
        <RegisterPage />
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import LoginPage from './loginForm.vue';
  import RegisterPage from './register.vue';
  
  export default {
    data() {
      return {
        isLogin: true,
      };
    },
    components: {
      LoginPage,
      RegisterPage,
    },
  };
  </script>
  
  <style scoped>
  .auth-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    width: 100vw;
    flex-direction: column;
  }
  
  .slider {
    position: relative;
    display: flex;
    justify-content: space-between;
    width: 100%;
    max-width: 400px;
    margin-bottom: 0.1rem;
    height: 50px;
    background: #e6f7ff;
    border-radius: 25px;
    overflow: hidden;
  }
  
  .slide-button {
    flex: 1;
    border: none;
    background: transparent;
    height: 100%;
    font-size: 16px;
    cursor: pointer;
  }
  
  .slider-background {
    position: absolute;
    width: 50%;
    height: 100%;
    transition: transform 0.4s;
    background: #1890ff;
    opacity: 0.3;
  }
  
  .active {
    color: black;
  }
  </style>