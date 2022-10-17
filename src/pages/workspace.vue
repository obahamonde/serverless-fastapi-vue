<script setup lang="ts">
import { useAuth0 } from "@auth0/auth0-vue";
const { getAccessTokenSilently: token } = useAuth0();
const uploads = ref(useRequest(token)("upload").json().data);
const onUpload = (urls: any) => {
  uploads.value = useRequest(token)("upload").json().data;
};
const onDelete = (url: string) => {
  useRequest(token)("upload?url=" + encodeURIComponent(url), {
    method: "DELETE",
  }).json();
  uploads.value = useRequest(token)("upload").json().data;
};
</script>
<template>
  <Upload @upload="onUpload" />
  <section grid4 p-8 ml-74 gap-2 b-2 h-screen>
    <div v-for="upload in unref(uploads)" col start>
      <Ico
        icon="mdi-delete"
        @click="onDelete(upload)"
        cp
        x1
        scale
        hover:text-danger
      />
      <img
        :src="upload"
        h-32
        v-if="
          upload.endsWith('.png') ||
          upload.endsWith('.jpg') ||
          upload.endsWith('.jpeg') ||
          upload.endsWith('.gif') ||
          upload.endsWith('.svg')
        "
      />
      <audio
        :src="upload"
        controls
        v-else-if="
          upload.endsWith('.mp3') ||
          upload.endsWith('.wav') ||
          upload.endsWith('.ogg')
        "
      />
      <video
        :src="upload"
        controls
        v-else-if="
          upload.endsWith('.mp4') ||
          upload.endsWith('.webm') ||
          upload.endsWith('.ogg')
        "
      />
      <iframe
        :src="upload"
        frameborder="0"
        v-else-if="upload.endsWith('.pdf')"
      />
      <a
        :href="upload"
        target="_blank"
        class="text-secondary hover:text-success"
        v-else
        ><Ico icon="mdi-file" x6
      /></a>
      <span text-xs>{{ upload.slice(upload.lastIndexOf("/") + 1) }}</span>
    </div>
  </section>
</template>
