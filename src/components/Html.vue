<template>
  <div col w-screen h-screen top-0 fixed>
    <div class="h-1/2">
      <prism-editor
        class="my-editor"
        v-model="editorCode"
        :highlight="highlighter"
        line-numbers
        @update="handleUpdate"
      >
      </prism-editor>
    </div>
    <iframe :src="url" class="h-1/2" frameborder="0" allowfullscreen></iframe>
  </div>
</template>
<script setup>
import { PrismEditor } from "vue-prism-editor";

// import highlighting library (you can use any library you want just return html string)
import prism from "prismjs";
import "prismjs/themes/prism-tomorrow.css"; // import syntax highlighting styles
const { data } = useFetch("api/static/index.html").text();
const editorCode = ref(data);
const url = computed(() => {
  return "data:text/html;charset=utf-8," + encodeURIComponent(editorCode.value);
});
const highlighter = (code) => {
  return prism.highlight(code, prism.languages.js);
};
</script>
<style scoped>
.my-editor {
  background: #2d2d2d;
  color: #ccc;
  font-family: Fira code, Fira Mono, Consolas, Menlo, Courier, monospace;
  font-size: 14px;
  line-height: 1.5;
  height: 100%;
}
.prism-editor__textarea:focus {
  outline: none;
}
.mb-4 {
  margin-bottom: 1rem;
}
</style>
