<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const store = useAuthStore()
const logout = store.logOut
</script>

<template>
  <div>
    <b-navbar class="navbar sticky-top navbar-expand-lg navbar-dark bg-dark">
      <b-navbar-brand href="#">Your App</b-navbar-brand>
      <ul class="navbar-nav">
        <li class="nav-item">
          <RouterLink class="nav-link" to="/">Home</RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink class="nav-link" to="/about">About</RouterLink>
        </li>
        <li class="nav-item" v-if="store.isAdmin">
          <RouterLink class="nav-link" to="/users">Users</RouterLink>
        </li>
      </ul>
      <div class="navbar-nav ms-auto">
        <div v-if="!store.user">
          <b-button @click="$router.push('login')">
            <i class="bi-person"></i>
          </b-button>
        </div>
        <div v-else>
          <b-button
            class="btn btn-secondary"
            data-bs-toggle="dropdown"
            aria-expanded="false"
            >{{ store.user?.email }}
          </b-button>
          <ul class="dropdown-menu dropdown-menu-end">
            <li>
              <div class="dropdown-item">Profile</div>
              <!--              <RouterLink class="dropdown-item" to="/profile"-->
              <!--                >Profile</RouterLink-->
              <!--              >-->
            </li>
            <li>
              <b-button @click="logout" class="dropdown-item">
                Logout
              </b-button>
            </li>
          </ul>
        </div>
      </div>
    </b-navbar>
    <div class="p-4 px-2 d-flex justify-content-center">
      <RouterView></RouterView>
    </div>
  </div>
</template>
