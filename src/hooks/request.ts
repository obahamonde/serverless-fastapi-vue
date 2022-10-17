import { createFetch } from "@vueuse/core";

export const useRequest = (tokenGetter: () => Promise<string>) => {
  const request = createFetch({
    baseUrl: "/api/",
    options: {
      async beforeFetch({ options }) {
        const token = await tokenGetter();
        options.headers = {
          ...options.headers,
          Authorization: `Bearer ${token}`,
        };
        return { options };
      },
    },
    fetchOptions: {
      mode: "cors",
    },
  });

  return request;
};
