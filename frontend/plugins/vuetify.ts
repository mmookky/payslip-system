import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import "@mdi/font/css/materialdesignicons.css";
import "vuetify/styles";

export default defineNuxtPlugin((app) => {
  const vuetify = createVuetify({
    components,
    directives,
    theme: {
      defaultTheme: "light",
      themes: {
        light: {
          colors: {
            primary: "#E65100",
            secondary: "#1565C0",
            deep_blue: "#0B2D72",
            honey: "#FFFAF0",
            sky: "#F2F9FF",
          },
        },
      },
    },
  });
  app.vueApp.use(vuetify);
});
