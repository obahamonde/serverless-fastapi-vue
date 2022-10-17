<script setup lang="ts">
import { useAuth0 } from "@auth0/auth0-vue";
const { user, logout, isAuthenticated, loginWithRedirect } = useAuth0();
const show = ref(false);
const router = useRouter();
</script>
<template>
  <nav
    class="row center rou bl fixed w-full h-16 bg-success animate-fade-in-up"
    v-if="isAuthenticated"
  >
    <div
      :class="
        show
          ? 'h-32 w-32 rounded-b rounded-full translate-y--8 bg-success col center'
          : 'h-32 w-32 rounded-full translate-y--8 bg-success col center'
      "
    >
      <img
        :src="user.picture"
        alt="logo"
        width="100"
        class="dark:invert animate-fade-in rf cp"
        @click="router.push('/profile')"
      />
    </div>
    <Ico
      icon="mdi-logout"
      class="x2 text-warning hover:text-danger justify-end right-0 absolute m-2 cp"
      @click="logout()"
    />
  </nav>
  <nav
    class="row center rou bl fixed w-full h-16 bg-success animate-fade-in-up"
    v-else
  >
    <div class="h-32 w-32 rounded-full translate-y--8 bg-success col center">
      <Ico
        icon="mdi-login"
        class="x2 text-success hover:text-secondary justify-end right-0 absolute m-2 cp"
        @click="loginWithRedirect()"
      />
    </div>
  </nav>
  <nav
    v-else
    class="row center rou bl fixed w-full h-16 bg-success animate-fade-in-up"
  >
    <div class="h-32 w-32 rounded-full translate-y--8 bg-success col center">
      <Ico
        icon="mdi-login"
        class="x2 text-success hover:text-secondary justify-end right-0 absolute m-2 cp"
        @click="loginWithRedirect()"
      />
    </div>
  </nav>
  <div v-else></div>
</template>
