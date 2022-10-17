<script setup lang="ts">
useHead({
  title: "Vipere",
  meta: [
    {
      name: "description",
      content: "Starter for web development with Vite and Python",
    },
  ],
  link: [
    {
      rel: "icon",
      href: "/favicon.ico",
    },
  ],
});
</script>

<template>
  <RouterView />
</template>

<style global>
html,
body,
#app {
  height: 100%;
  margin: 0;
  padding: 0;
  overflow-x: hidden;
}
html.dark {
  background: #121212;
  color-scheme: dark;
}

#nprogress {
  pointer-events: none;
}
.prose pre:not(.shiki) {
  padding: 0;
}

.prose .shiki {
  font-family: "DM Mono", monospace;
  font-size: 1.2em;
  line-height: 1.4;
}

.prose img {
  width: 100%;
}

.shiki-light {
  background: #f8f8f8 !important;
}
.shiki-dark {
  background: #0e0e0e !important;
}

html.dark .shiki-light {
  display: none;
}

html:not(.dark) .shiki-dark {
  display: none;
}

.router-link-exact-active {
  @apply text-amber;
}

::-webkit-scrollbar {
  width: 10px;
}

::-webkit-scrollbar-track {
  box-shadow: inset 0 0 5px grey;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb {
  background: cyan;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: teal;
}
</style>
