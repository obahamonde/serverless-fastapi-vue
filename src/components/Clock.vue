<script setup lang="ts">
const now = useNow();
watchEffect(() => {
  unref(now).getHours() > 18 ? useDark() : usePreferredDark();
});
</script>
<template>
  <strong
    cp
    z-50
    tr
    fixed
    text-secondary
    m-4
    hover:text-danger
    title="Don't Click Me"
    >{{ now.toLocaleTimeString().replace(/:\d\d$/, "") }}</strong
  >
</template>
