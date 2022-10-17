<script setup>
const input = ref("")
const results = ref([])
const page = ref(0)
const lang = ref('en-US')
const speech = useSpeechRecognition({
    lang,
    continuous: true,
})
const SpeechGrammarList = window.SpeechGrammarList || window.webkitSpeechGrammarList
const speechRecognitionList = new SpeechGrammarList()
speechRecognitionList.addFromString(1)
speech.recognition.grammars = speechRecognitionList
const toggle = ref(false)
const { isListening, stop, result } = speech
const selectedLanguage = ref(lang.value)
watch(lang, lang => selectedLanguage.value = lang)
watch(isListening, isListening => isListening ? null : selectedLanguage.value = lang.value)
watchEffect(() => input.value ? null : results.value = [])
const start = () => {
    input.value = "..."
    speech.start()
}
const query = computed(() => {
    if (!isListening.value) {
        return input.value.length > 0 ? input.value.split(" ").join("+") : "";
    }
    else if (isListening) {
        return result.value.split(" ").join("+")
    }
})
const toggler = () => {
    toggle.value = !toggle.value
    results.value = []
    input.value = ""
}
const search = () => {
    const { data } = useFetch(`api/search/${unref(lang)}/${unref(query)}/${unref(page)}`).json()
    results.value = data
}
</script>
<template>
    <div
        :class="!toggle ? 'bg-gray-500 p-2 rf tr fixed m-4 mt-12':'z-50 bg-light shadow-lg shadow-gray-500 rounded-xl p-1 tl pt-8 fixed w-75 h-full'">
        <div col center>
            <div row center border-gray-500 b-2 rounded-xl hover-bg-transparent backdrop-blur-md p-1>
                <div i-carbon-search cp scale @click.prevent="toggler"
                    :class="!toggle ? 'text-white p-2 rf':'text-secondary'" />
                <h1 row v-if="toggle" fade-in-left><input type="search" bg-transparent no-outline text-secondary
                        dark:text-primary v-model="input" @keyup.enter="search" @keyup.escape="toggler" />
                    <span row center>
                        <Ico icon="mdi-microphone" text-xl text-secondary cp dark:text-primary v-if="!isListening"
                            @click="start" />
                        <Ico icon="mdi-microphone-off" text-xl text-secondary cp dark:text-primary v-else
                            @click="search();stop()" />
                    </span>
                </h1>
            </div>
        </div>
        <div row center pb-2 v-if="input" fade-in-down mt-2 col backdrop-blur-lg> <label :id="lang" class="radio">
                <input v-model="lang" value="en" type="radio" hidden>
                <img src="/images/us.svg" mx-1 cp scale @click="lang='en';page=1;search()"
                    :class="{ 'shadow-black scale-125 dark:shadow-white shadow-md': lang === 'en' }" />

                <span>
                </span>
            </label>
            <label :id="lang" class="radio">
                <input v-model="lang" value="fr" type="radio" hidden>
                <img src="/images/fr.svg" mx-1 cp scale @click="lang='fr';page=1;search()"
                    :class="{ 'shadow-black scale-125 dark:shadow-white shadow-md': lang === 'fr' }" />

            </label>
            <label :id="lang" class="radio">
                <input v-model="lang" value="es" type="radio" hidden>
                <img src="/images/pe.svg" mx-1 cp scale @click="lang = 'es';page=1;search()"
                    :class="{ 'shadow-black scale-125 dark:shadow-white shadow-md': lang === 'es' }">

            </label>
        </div>
        <div v-if="input" col backdrop-blur-lg>
            <div v-for="r in unref(results)" col>
                <a :href="r.url" text-xs underline m-2 text-success hover:text->{{ r.summary }}</a>
            </div>
            <div row text-secondary cp dark:text-primary center mt-6 v-if="(unref(results).length > 0)">
                <Ico icon="mdi-chevron-left" text-xl mx-1 text-secondary cp dark:text-primary v-if="page > 0"
                    @click="page -= 1;search()" />
                {{ page + 1 }}
                <Ico icon="mdi-chevron-right" text-xl mx-1 text-secondary cp dark:text-primary v-if="page < 10"
                    @click="page +=1;search()" />
            </div>
        </div>
    </div>
</template>
