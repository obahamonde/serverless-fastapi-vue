<script setup lang="ts">
const toggler = ref(false);
const nav = reactive({
  iconClass: toggler.value
    ? "tl fixed x2 m-4 p-1 scale-125 text-secondary fade-in"
    : "tl fixed x2 m-1 rounded  m-4 p-1 scale-125 z-50  fade-in-left",
  bar: toggler.value
    ? "hidden"
    : "h-screen  col w-17 tl fixed bg-success fade-in-left",
});
</script>
<template>
  <button @click.prevent="toggler = !toggler">
    <Ico
      :icon="toggler ? 'mdi-menu' : 'mdi-close'"
      :class-name="
        toggler
          ? 'tl fixed x2 m-4 p-1 scale-125 text-secondary dark:text-light z-50 fade-in-down'
          : 'tl fixed x2 m-1 rounded  m-4 p-1 scale-125 z-50 dark:text-light fade-in-left'
      "
    />
  </button>
  <section v-if="toggler">HELLO</section>
  <section :class="nav.bar" pt-16 z-50 v-else text-primary>
    <Router-Link to="/">
      <Ico icon="mdi-home" class="m-4 p-1 z-50 x2 scale-110 dark:text-light" />
    </Router-Link>
    <Router-Link to="/code">
      <Ico icon="mdi-xml" class="m-4 p-1 z-50 x2 scale-110 dark:text-light" />
    </Router-Link>
    <Router-Link to="/deploy">
      <Ico
        icon="eos-icons:code-deploy"
        class="m-4 p-1 z-50 x2 scale-110 dark:text-light"
      />
    </Router-Link>
  </section>
</template>
