<template>
  <div row>
    <div class="w-1/2">
      <prism-editor
        class="my-editor"
        v-model="editorCode"
        :highlight="highlighter"
        line-numbers
      >
      </prism-editor>
    </div>
    <div v-html="editorCode" class="w-1/2 bg-white h-94vh w-75vw"></div>
  </div>
</template>

<script>
import { PrismEditor } from "vue-prism-editor";
import prism from "prismjs";

import { defineComponent, onMounted, ref } from "vue";
export default defineComponent({
  components: {
    PrismEditor,
  },
  setup() {
    const editorCode = ref(
      "<h1 class='title'>Hello World!</h1><style>.title{color:purple;font-size:3rem;text-align:center;margin-top:6rem;}</style>"
    );
    const highlighter = (code) => {
      return prism.highlight(code, prism.languages.js);
    };
    return { editorCode, highlighter };
  },
});
</script>

<style>
.my-editor {
  /* we dont use `language-` classes anymore so thats why we need to add background and text color manually */
  background: #2d2d2d;
  color: #ccc;

  /* you must provide font-family font-size line-height. Example: */
  font-family: Fira code, Fira Mono, Consolas, Menlo, Courier, monospace;
  font-size: 14px;
  line-height: 1.5;
  padding-top: 10px;
  height: 100%;
}

/* optional class for removing the outline */
.prism-editor__textarea:focus {
  outline: none;
}

.mb-4 {
  margin-bottom: 1rem;
}
</style>
