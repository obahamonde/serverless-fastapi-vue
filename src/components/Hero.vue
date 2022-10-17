<template>
  <div col center z-50 top-16 fixed>
    <h1 m-4 font-script text-3xl text-warning>{{ props.brand }}</h1>
    <img :src="props.logo" alt="logo" width="100" dark:invert animate-fade-in />
    <section m-8 text-2xl font-script text-success col center>
      <h1 my-4 text-shadow-xl shadow-gray-500 text-center>
        {{ props.cta }}
      </h1>
      <h2 my-4 text-shadow-xl shadow-gray-500 text-center>
        {{ props.slug }}
      </h2>
      <button btn-post font-sans rounded-lg m-8 @click="start()">
        Get Started
      </button>
    </section>
    <Rocket z-50 tl fixed h-screen w-screen v-if="toggle" />
  </div>
</template>

<script setup lang="ts">
import { useAuth0 } from "@auth0/auth0-vue";
const { loginWithRedirect } = useAuth0();
const props = defineProps<{
  cta: string;
  slug: string;
  brand: string;
  logo: string;
}>();

const toggle = ref(false);
const start = async () => {
  toggle.value = true;
  setTimeout(() => {
    toggle.value = false;
  }, 3000);
  setTimeout(async () => {
    await loginWithRedirect();
  }, 2500);
};
</script>
