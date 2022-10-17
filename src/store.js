import { acceptHMRUpdate, defineStore } from "pinia";
export const useState = defineStore("state", () => {
    const state = reactive({});
    const setState = (key, value) => {
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
