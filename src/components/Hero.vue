<template>
  <div col center z-50 top-16 fixed dark:invert> 
    <h1 m-4 font-script text-3xl text-warning>{{ props.brand }}</h1>
    <img :src="props.logo" alt="logo" width="300"  animate-fade-in />
    <section m-8 text-2xl font-script text-success col center>
      <h1 my-4 text-shadow-xl shadow-gray-500 text-center>
        {{ props.cta }}
      </h1>
      <h2 my-4 text-shadow-xl row center shadow-gray-500 text-center>
        {{ props.slug }} <Ico :icon="props.icon" mx-2 />
      </h2>
      <button btn-post font-sans rounded-lg m-8 @click="start()">
        Get Started
      </button>
    </section>

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
  icon: string;
}>();

const start = async () => {
    await loginWithRedirect();
};
</script>
