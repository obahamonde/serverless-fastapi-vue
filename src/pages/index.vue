<script setup lang="ts">
import { useAuth0 } from "@auth0/auth0-vue";
import { useState } from "~/store";
const { isAuthenticated, user } = useAuth0();
const { setState } = useState();
setState("user", user);
const customer = reactive({
  brand: "Boilerplate",
  logo: "/logo.svg",
  cta: "⚡The Best Cloud is no Cloud",
  slug: "☁️ Deliver value faster the Full-Stack Serverless starter kit.",
});
const foo = ref(true);
useTitle("Home");
</script>
<template>
  <div v-if="isAuthenticated" class="col center">
    <Nav />
    <Dock />
  </div>
  <div v-else h-screen w-screen col center>
    <ThreeSlider />
    <Hero
      :brand="customer.brand"
      :logo="customer.logo"
      :cta="customer.cta"
      :slug="customer.slug"
      v-if="foo"
    />
  </div>
</template>
<route lang="yaml">
meta:
  layout: home
</route>
