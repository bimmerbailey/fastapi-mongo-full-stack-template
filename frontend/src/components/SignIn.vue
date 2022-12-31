<template>
  <div>
    <b-card class="auth">
      <form>
        <h3>Sign In</h3>
        <b-form-group>
          <label>Email address</label>
          <input
            type="email"
            class="form-control form-control-lg"
            v-model="username"
          />
        </b-form-group>
        <b-form-group>
          <label>Password</label>
          <input
            type="password"
            class="form-control form-control-lg"
            v-model="password"
          />
        </b-form-group>
        <b-button class="btn btn-lg btn-block" @click="login">
          Sign In
        </b-button>
        <p class="forgot-password text-right mt-2 mb-4">
          <RouterLink to="/forgot-password">Forgot password ?</RouterLink>
        </p>
        <p class="forgot-password text-right">
          Don't Have an Account
          <RouterLink :to="{ name: 'signup' }">sign up?</RouterLink>
        </p>
        <div class="social-icons">
          <ul>
            <li>
              <a href="#"><i class="bi bi-google"></i></a>
            </li>
            <li>
              <a href="#"><i class="bi bi-facebook"></i></a>
            </li>
            <li>
              <a href="#"><i class="bi bi-twitter"></i></a>
            </li>
          </ul>
        </div>
      </form>
    </b-card>
  </div>
</template>

<script lang="ts">
import { RouterLink } from 'vue-router'
import { defineComponent } from 'vue'
// import { AuthApi } from "@/api";
// import type Login from "@/interfaces/Auth";
import { useAuthStore } from '@/stores/auth'

export default defineComponent({
  components: {
    RouterLink,
  },
  data() {
    return {
      username: '',
      password: '',
    }
  },
  methods: {
    login() {
      useAuthStore().login(this.username, this.password)
      // AuthApi.login(this.username, this.password)
      //   .then((resp) => {
      //     return resp.json();
      //   })
      //   .then((res: Login) => {
      //     console.log(res);
      //   });
    },
  },
})
</script>

<style scoped>
.vertical-center {
  display: flex;
  text-align: left;
  justify-content: center;
  flex-direction: column;
}

.inner-block {
  width: 450px;
  margin: auto;
  background: #ffffff;
  box-shadow: 0px 14px 80px rgba(34, 35, 58, 0.2);
  padding: 40px 55px 45px 55px;
  border-radius: 15px;
  transition: all 0.3s;
}

.vertical-center .form-control:focus {
  border-color: #2554ff;
  box-shadow: none;
}

.vertical-center h3 {
  text-align: center;
  margin: 0;
  line-height: 1;
  padding-bottom: 20px;
}

label {
  font-weight: 500;
}

.forgot-password,
.forgot-password a {
  text-align: center;
  font-size: 13px;
  padding-top: 10px;
  color: #7a7a7a;
}

.forgot-password a {
  color: #2554ff;
}

.social-icons {
  text-align: center;
  font-weight: 300;
  font-size: 1.5em;
  color: #222222;
}

.social-icons ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.social-icons ul li {
  display: inline-block;
  zoom: 1;
  width: 65px;
  vertical-align: middle;
  border: 1px solid #e3e8f9;
  font-size: 15px;
  height: 40px;
  line-height: 40px;
  margin-right: 5px;
}

.social-icons ul li a {
  display: block;
  font-size: 1.4em;
  margin: 0 5px;
  text-decoration: none;
}

.social-icons ul li a i {
  -webkit-transition: all 0.2s ease-in;
  -moz-transition: all 0.2s ease-in;
  -o-transition: all 0.2s ease-in;
  -ms-transition: all 0.2s ease-in;
  transition: all 0.2s ease-in;
}

.social-icons ul li a:focus i,
.social-icons ul li a:active i {
  transition: none;
  color: #222222;
}
</style>
