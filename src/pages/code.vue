<script setup lang="ts">
import { useState } from "~/store";
const { state, setState } = useState();
const html = ref(false);
const python = ref(false);
onMounted(() => {
  setState("menu", true);
  return state;
});

const fetchHtml = () => {
  html.value = !html.value;
  python.value = false;
};
const fetchPython = () => {
  python.value = !python.value;
  html.value = false;
};
</script>
<template>
  <section
    class="col pl-2 tl fixed h-full ml-16 w-32 bg-gray-300 rounded-lg bg-gray-300 animate-fade-in-left"
  >
    <nav class="col start gap-6 my-8">
      <h1 row @click="fetchHtml" cp>
        <Ico icon="logos:html-5" mx-2 text-2xl /><span class="text-sm text-info"
          >index.html</span
        >
      </h1>
      <h1 row @click="fetchPython" cp>
        <Ico icon="logos:python" mx-2 text-2xl /><span class="text-sm text-info"
          >app.py</span
        >
      </h1>
    </nav>
  </section>
  <div ml-48>
    <Html v-if="html" endpoint="html" contentType="text/html" />
    <Python v-if="python" endpoint="python" contentType="text/x-python" />
  </div>
</template>
<style global>
[uncloak] {
  display: none;
}
</style>
<route lang="yaml">
meta:
  layout: code
</route>
