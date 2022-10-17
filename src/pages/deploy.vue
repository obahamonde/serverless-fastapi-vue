<template>
<div id="container">
{{state}}
</div>
</template>
<script setup lang="ts">
import { useState } from '~/store' 
const { state } = useState();

</script>
