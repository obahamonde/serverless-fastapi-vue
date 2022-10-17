<template>
  <div v-if="show">
    <transition>
      <div :bg="props.bg" toast>
        {{ toast }}
        <Ico icon="mdi-check-circle" m-1 cp @click="hide" />
      </div>
    </transition>
  </div>

  <audio hidden src="/audio/200.wav" id="notificationSound"></audio>
</template>

<script setup lang="ts">
const props = defineProps<{
  timeout: number;
  bg: string;
  toast: string;
}>();
const timer = ref(props.timeout);
const show = ref(props.timeout > 0);

const notificationSound = () => {
  const audio = document.getElementById(
    "notificationSound"
  ) as HTMLAudioElement;
  timer.value > 0 ? audio.play() : audio.pause();
};

const hide = () => {
  show.value = false;
};

onMounted(() => {
  notificationSound();
  setInterval(() => {
    timer.value--;
  }, 1000);
});

watch(timer, (val) => {
  if (val <= 0) {
    hide();
  }
});
</script>
