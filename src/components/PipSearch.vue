<script setup lang="ts">
import { ComputedRef, Ref } from "vue";
const search = ref("");
const results = ref([]) as Ref<any[]>;
const page = ref(1);
const lang = ref("en-US");
const speech = useSpeechRecognition({
  lang,
  continuous: true,
});
const SpeechGrammarList =
  window.SpeechGrammarList || window.webkitSpeechGrammarList;
const speechRecognitionList = new SpeechGrammarList();
speechRecognitionList.addFromString(1);
speech.recognition!.grammars = speechRecognitionList;

const toggle = ref(false);
const { isListening, stop, result } = speech;
const selectedLanguage = ref(lang.value);
watch(lang, (lang) => (selectedLanguage.value = lang));
watch(isListening, (isListening) =>
  isListening ? null : (selectedLanguage.value = lang.value)
);
watchEffect(() => (search.value ? null : (results.value = [])));
const start = () => {
  search.value = "";
  speech.start();
};
const query: ComputedRef<string | undefined> = computed(() => {
  if (!isListening.value) {
    return search.value.length > 0 ? search.value.split(" ").join("+") : "";
  } else if (isListening) {
    return result.value.split(" ").join("+");
  }
});

function handleToggle() {
  toggle.value = !toggle.value;
  results.value = [];
  search.value = "";
}

function searchQueryspeech() {
  const { data } = useFetch(
    `api/search/pip/${unref(query)}/${unref(page)}`
  ).json();
  results.value = data;
  stop();
}

function searchQuery() {
  const { data } = useFetch(
    `api/search/pip/${unref(query)}/${unref(page)}`
  ).json();
  results.value = data;
}

function nextPage() {
  page.value += 1;
  searchQuery();
}

function prevPage() {
  page.value -= 1;
  searchQuery();
}
</script>
<template>
  <div
    col
    :class="
      !toggle
        ? 'bg-gray-500 p-2 rf tr fixed m-4 mt-12'
        : 'w-auto z-50 rounded-xl m-auto p-1'
    "
  >
    <div col center>
      <div row center border-gray-500 b-2 rounded-xl hover-bg-transparent>
        <div
          i-carbon-search
          cp
          scale
          @click.prevent="handleToggle"
          :class="!toggle ? 'text-white p-2 rf' : 'text-secondary'"
        />
        <h1 row v-if="toggle" fade-in-left>
          <input
            type="search"
            bg-transparent
            no-outline
            text-secondary
            dark:text-primary
            v-model="search"
            @keyup.enter="searchQuery"
            @keyup.escape="handleToggle"
          />
          <span row center>
            <Ico
              icon="mdi-microphone"
              text-xl
              text-secondary
              cp
              dark:text-primary
              v-if="!isListening"
              @click="start"
            />
            <Ico
              icon="mdi-microphone-off"
              text-xl
              text-secondary
              cp
              dark:text-primary
              v-else
              @click="searchQueryspeech"
            />
          </span>
        </h1>
      </div>
    </div>
    <div v-if="search" grid4 m-16 gap-4>
      <div v-for="r in unref(results)" bg-secondary p-4 rounded-lg shadow col>
        <h1 text-xs underline m-2 hover:text-success cp>{{ r.name }}</h1>
        <small text-xs m-2>{{ r.version }}</small>
        <p text-xs m-2>{{ r.description }}</p>
      </div>
      <div row center mt-6 v-if="unref(results).length > 0">
        <Ico
          icon="mdi-chevron-left"
          text-xl
          mx-1
          text-secondary
          cp
          dark:text-success
          v-if="page > 1"
          @click="prevPage"
        />
        <span v-if="page > 0">{{ page }}</span>
        <Ico
          icon="mdi-chevron-right"
          text-xl
          mx-1
          text-secondary
          cp
          dark:text-success
          v-if="page < 10"
          @click="nextPage"
        />
      </div>
    </div>
  </div>
</template>
