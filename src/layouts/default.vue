<script setup>
import { useAuth0 } from "@auth0/auth0-vue";
const { isAuthenticated } = useAuth0();
</script>

<template>

  <Nav />
  <RouterView />
  <Search />
  <Clock />
  <Dock />
</template>
