<script setup lang="ts">
const query = ref('')
const queryString = computed(() => query.value.split(' ').join('+'))
const searchResults = ref<any[]>([])
const search = async () => {
    const { data } = await useFetch(
        "/api/github/" + queryString.value
    ).json()
    searchResults.value = unref(data)
}
watchEffect(() => {
    if (query.value == "") {
        searchResults.value = []
    }
})
</script>
<template>
    <main col center animate slide-down>
        <h1 row center text-3xl m-8>
            <Ico icon="mdi-github" text-6xl mx-4 /> Lookup
        </h1>
        <h1 row center bg-gray-500 b-2 p-2 m-2 rounded-xl text-lg><input type='text' v-model='query'
                @keyup.enter='search' @keyup.esc="searchResults = []; queryString=''" @keyup.backspace="search" bg-gray-500 outline-none
                placeholder="Search Repos..." /></h1>
        <section grid3 gap-8 p-16 pl-32 font-bold>
            <div v-for='result in searchResults' :key='result.id' shadow-gray shadow-md p-4 rounded>
                <h1 m-2>{{ result.name }}</h1>
                <p m-2>{{ result.owner }}</p>
                <a :href="result.avatar"><img :src="result.avatar" x3 rf m-2 /></a>
                <a m-2 :href="result.url" text-secondary dark:text-success text-xs hover:underline>{{ result.url }}</a>
                <p m-2>{{ result.description }}</p>

                <p grid4 gap-2 p-4 text-xs>
                <p col text-sm center>
                    <sm text-xs>Stars</sm>
                    <Ico icon="mdi-star" x2 text-amber /> {{ result.stars }}
                </p>
                <p col text-sm center>
                    <sm text-xs>Forks</sm>
                    <Ico icon="mdi-git" x2 text-red /> {{ result.forks }}
                </p>
                <p col text-sm center>
                    <sm text-xs>Issues</sm>
                    <Ico icon="mdi-bug" x2 text-red /> {{ result.issues }}
                </p>
                <p col text-sm center>
                    <sm text-xs>Size</sm>
                    <Ico icon="mdi-zip-box" x2 text-red />{{ result.size }}
                </p>
                </p>
                <h1 text-sm text-center my-4 underline v-if="result.topics.length > 0">Topics</h1>
                <p grid3>
                <p v-for="i in result.topics">
                <p text-xs text-center>{{ i }}</p>
                </p>
                </p>
                <h1 text-sm text-center my-4 underline v-if="result.languages.length > 0">Languages</h1>
                <p grid3>

                <p v-for="r in result.languages" col center text-sm scale-75 font-bold>
                    {{ Object.keys(r).pop() }} {{ Number(Object.values(r).pop()) / Number(result.languages.map((i:
        any) => Object.values(i).pop()).reduce((a: any, b: any) => a + b)) * 100 | round
                    }}% </p>


                </p>
            </div>
        </section>
    </main>
</template>
