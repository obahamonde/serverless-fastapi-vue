import { acceptHMRUpdate, defineStore } from "pinia";

export const useState = defineStore("state", () => {
  const state = reactive({}) as any;
  const setState = (key: string, value: any) => {
    state[key] = value;
  };
  return {
    state,
    setState,
  };
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useState, import.meta.hot));
}
