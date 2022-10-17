<script setup lang="ts">
const router = useRouter();
</script>

<template>
  <main>
    <div>
      <div i-carbon-warning inline-block />
    </div>
    <RouterView />
    <div>
      <button @click="router.back()">Back</button>
    </div>
  </main>
</template>
