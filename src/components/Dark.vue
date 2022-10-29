<template>

    <Ico
      icon="mdi:lightbulb-on"
      v-if="isDark"
      @click="toggleDark()"
    />
    <Ico
      icon="mdi:lightbulb-off-outline"
      v-else
      @click="toggleDark()"
    />

</template>
