<template>
    <div>
        <form @submit.prevent="register" class="login-form">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" v-model="formData.username" />
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="formData.password" />
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="confirmPassword" v-model="formData.confirmPassword" />
            </div>
            <button type="submit">Register</button>
        </form>
        <p v-if="passwordMismatch">Passwords do not match!</p>
        <p v-else-if="errorMessage">{{ errorMessage }}</p>
    </div>
</template>

<script lang="ts">
    import { Component, Vue } from 'nuxt-property-decorator';
   import axios from 'axios';

   @Component
    export default class LoginPage extends Vue {
    formData: { username: string; password: string; confirmPassword: string } = {
      username: '',
      password: '',
      confirmPassword: '',
    };
    showErrorMessage: boolean = false;
    errorMessage: string = '';
    passwordMismatch: boolean = false;
  
    async register() {
            if (this.formData.password !== this.formData.confirmPassword) {
                this.passwordMismatch = true;
                return;
            }
            this.passwordMismatch = false;
            try {
                const response = await axios.post('http://localhost:8000/api/v1/register', {
                    username: this.formData.username,
                    password: this.formData.password,
                });
                // handle successful registration
                if (response.status === 200) {
                    location.reload();
                }
                else {
                    this.errorMessage = response.data.message;
                }
            }
            catch (error) {
            // handle error
            }
        }
    };
</script>

<style scoped lang="scss">
    @import "./style.css";
</style>