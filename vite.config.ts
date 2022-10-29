import path from "path";
import { defineConfig } from "vite";
import Vue from "@vitejs/plugin-vue";
import Pages from "vite-plugin-pages";
import generateSitemap from "vite-ssg-sitemap";
import Layouts from "vite-plugin-vue-layouts";
import Components from "unplugin-vue-components/vite";
import AutoImport from "unplugin-auto-import/vite";
import Markdown from "vite-plugin-vue-markdown";
import Inspect from "vite-plugin-inspect";
import LinkAttributes from "markdown-it-link-attributes";
import Unocss from "unocss/vite";
import Shiki from "markdown-it-shiki";

export default defineConfig({
  resolve: {
    alias: {
      "~/": `${path.resolve(__dirname, "src")}/`,
    },
  },

  server: {
    proxy: {
      "/api": {
        target: "https://ks5stj5f5bqcw235o2gehbcz5q0estdg.lambda-url.us-east-1.on.aws/",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },

  plugins: [
    Vue({
      include: [/\.vue$/, /\.md$/],
      reactivityTransform: true,
    }),
    Pages({
      extensions: ["vue", "md", "html"],
    }),
    Layouts(),
    AutoImport({
      imports: [
        "vue",
        "vue-router",
        "vue/macros",
        "@vueuse/head",
        "@vueuse/core",
      ],
      dts: "src/auto-imports.d.ts",
      dirs: ["src/hooks", "src/store"],
      vueTemplate: true,
      
    }),
 
    Components({
      extensions: ["vue", "md","html"],
      include: [/\.vue$/, /\.vue\?vue/, /\.md$/, /\.html$/],
      dts: "src/components.d.ts",
    
    }),
    Unocss(),
    Markdown({
      wrapperClasses: "prose prose-sm m-auto text-left",
      headEnabled: true,
      markdownItSetup(md: {
        use: (
          arg0: any,
          arg1: {
            theme?: { light: string; dark: string };
            matcher?: (link: string) => boolean;
            attrs?: { target: string; rel: string };
          }
        ) => void;
      }) {
        // https://prismjs.com/
        md.use(Shiki, {
          theme: {
            light: "vitesse-light",
            dark: "vitesse-dark",
          },
        });
        md.use(LinkAttributes, {
          matcher: (link: string) => /^https?:\/\//.test(link),
          attrs: {
            target: "_blank",
            rel: "noopener",
          },
        });
      },
    }),
    Inspect(),
  ],
  ssgOptions: {
    script: "async",
    formatting: "minify",
    onFinished() {
      generateSitemap();
    },
  },

  ssr: {
    noExternal: ["workbox-window"],
  },
  assetsInclude: ["**/*.svg", "**/*.png", "**/*.jpg", "**/*.jpeg", "**/*.gif", "**/*.html"],
});
