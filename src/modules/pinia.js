import { createPinia } from "pinia";
import { createAuth0 } from "@auth0/auth0-vue";
export const install = ({ isClient, initialState, app }) => {
    const pinia = createPinia();
    app.use(pinia);
    app.use(createAuth0({
        domain: "dev-tvhqmk7a.us.auth0.com",
        client_id: "53p0EBRRWxSYA3mSywbxhEeIlIexYWbs",
        redirect_uri: window.location.origin,
    }));
    if (isClient)
        pinia.state.value = initialState.pinia || {};
    else
        initialState.pinia = pinia.state.value;
};
