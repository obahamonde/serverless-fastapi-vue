<script setup lang="ts">
const results = ref<any[]>([])
const domain = ref("")
const foo = ref(false)
const handle = async () => {
    if (domain.value.length > 0) {
        foo.value = true
        const { data } = await useFetch("/api/crawl/" + domain.value).json()
        results.value = unref(data)
        foo.value = false
    }
}

watchEffect(() => {
    if (domain.value == "") {
        results.value = []
    }
})
</script>
<template>
    <h1 row center text-3xl m-8>
        <img src="/logo.png" w-48 :class="foo ? 'animate-bounce' : ''">
    </h1>
    <p col center>
        <input type='text' v-model='domain' @keyup.enter='handle' @keyup.esc="results = []; domain = ''"
            bg-secondary outline-none mx-auto text-center p-2 rounded-lg text-light
            placeholder="Scrap Domains..." />
    </p>
    <section grid6 gap-2 ml-24 p-16>
   
        <div v-for="img in results.images" m-2 w-24>
        <img :src="img" m-2      />
    </div>
</section>
<section grid3 gap-2 ml-24 p-16>
<div v-for="link in results.links" m-2 text-xs text-secondary dark:text-success>
        <a :href="link" target="_blank" hover:underline>{{ link }}</a>
        </div>
        <section col center>
<p font-mono col center p-16 text-center mx-auto>

{{ results.text }}

</p>
</section>
</section>
</template>
