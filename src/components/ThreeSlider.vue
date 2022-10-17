<template>
  <Slider :images="images" />
</template>

<script setup lang="ts">
import { default as Slider } from "troisjs/src/components/sliders/Slider2.vue";

const images = ref([
  { src: "/images/1.jpg" },
  { src: "/images/2.jpg" },
  { src: "/images/3.jpg" },
]);
</script>
