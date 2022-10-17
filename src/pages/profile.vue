<script setup lang="ts">
import { useState } from "~/store";
const { state } = useState();
</script>
<template>
  <div m-12 mt-4 ml-32>
    <h1>{{ state.user.nickname }}</h1>
    <h2>{{ state.user.email }}</h2>
    <img :src="state.user.picture" rf x6 m-4 />
  </div>
</template>
<route lang="yaml">
meta:
  layout: profilepage
</route>
