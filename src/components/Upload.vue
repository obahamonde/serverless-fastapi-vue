<script setup lang="ts">
import { useAuth0 } from "@auth0/auth0-vue";
import { Ref } from "vue";
const files = ref([]) as Ref<File[]>;
const filesPreview = ref([]) as Ref<any[]>;
const { user, isAuthenticated } = useAuth0();
const timeout = 5;
const _show = ref(false);
const emit = defineEmits(["upload"]);
const urls = ref([]);
const onFileChange = (e: any) => {
  files.value = Array.from(e.target.files);
  files.value.forEach((file) => {
    const reader = new FileReader();
    reader.onload = () => {
      filesPreview.value.push({
        name: file.name,
        size: file.size,
        type: file.type,
        src: reader.result,
      });
    };
    reader.readAsDataURL(file);
  });
};
const onSubmit = async (e: any) => {
  e.preventDefault();
  files.value.forEach(async (file) => {
    const formData = new FormData();
    formData.append("file", file);
    const response = await useFetch("/api/upload/" + user.value.sub, {
      method: "POST",
      body: formData,
    }).json();
    urls.value = response.data as any;
    _show.value = true;
    emit("upload", urls.value);
    filesPreview.value = [];
  });
};
const onDragOver = (e: any) => {
  e.preventDefault();
  e.dataTransfer.dropEffect = "copy";
};
const onDragLeave = (e: any) => {
  e.preventDefault();
};
const onDrop = (e: any) => {
  e.preventDefault();
  files.value = Array.from(e.dataTransfer.files);
  files.value.forEach((file) => {
    const reader = new FileReader();
    reader.onload = () => {
      filesPreview.value.push({
        name: file.name,
        size: file.size,
        type: file.type,
        src: reader.result,
      });
    };
    reader.readAsDataURL(file);
  });
};
</script>
<template>
  <div
    v-if="isAuthenticated"
    class="mb-16 mt-16 w-72 col center bg-transparent p-1 shadow-light shadow-md cp tl fixed m-1 hover:border-solid"
    @upload="onUpload"
  >
    <div>
      <form @submit.prevent="onSubmit">
        <div row>
          <label
            @dragover.prevent="onDragOver"
            @dragleave.prevent="onDragLeave"
            @drop.prevent="onDrop"
            for="files"
            cp
            hover:underline
            >{{
              filesPreview.length > 0
                ? files
                    .reduce((acc, file) => acc + file.size / 1024, 0)
                    .toFixed(2) + " KB"
                : "Upload files"
            }}
            <input
              type="file"
              id="files"
              hidden
              @change="onFileChange"
              multiple
              accept="*/*"
          /></label>
          <div v-if="filesPreview.length > 0" row center>
            <label for="submit" @click="onSubmit" btn-post mx-2>Submit</label>
            <input type="submit" id="submit" hidden />
            <Ico
              icon="mdi-delete"
              @click="filesPreview = []"
              cp
              x1
              scale
              hover:text-danger
            />
          </div>
        </div>
      </form>
      <div>
        <ul grid3>
          <li
            v-for="(file, index) in filesPreview"
            class="bg-transparent p-1 col center m-2 rounded-lg shadow"
          >
            <button @click="filesPreview.splice(index, 1)">
              <Ico icon="mdi-delete" class="cp x1 scale hover:text-danger" />
            </button>
            <img :src="file.src" x4 v-if="file.type.startsWith('image')" />
            <audio
              :src="file.src"
              controls
              v-else-if="file.type.startsWith('audio')"
            />
            <video
              :src="file.src"
              controls
              v-else-if="file.type.startsWith('video')"
            />
            <div v-else>
              <Ico icon="mdi-file" cp x4 scale />
            </div>
            <div text-xs font-sans>{{ file.name.substring(0, 8) + "..." }}</div>
            <h2 text-xs font-serif scale-80>
              {{ (file.size / 1024).toFixed(2) }} KB
            </h2>
            <h3 text-xs font-mono scale-80>{{ file.type }}</h3>
          </li>
        </ul>
      </div>
    </div>
    <Toast
      bg="success"
      toast="Files Uploaded successfully!"
      :timeout="timeout"
      v-if="_show"
    />
  </div>
</template>
