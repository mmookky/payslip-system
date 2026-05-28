import { defineStore } from "pinia";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: null,
    role: null,
  }),

  getters: {
    isLoggedIn: (state) => !!state.token,
    isAdmin: (state) => state.role === "admin",
    isEmployee: (state) => state.role === "employee",
  },

  actions: {
    initAuth() {
      if (process.client) {
        const token = useCookie("token");
        const role = useCookie("role");
        this.token = token.value;
        this.role = role.value;
      }
    },

    setAuth(token, role) {
      this.token = token;
      this.role = role;
      const tokenCookie = useCookie("token", { maxAge: 60 * 60 * 8 });
      const roleCookie = useCookie("role", { maxAge: 60 * 60 * 8 });
      tokenCookie.value = token;
      roleCookie.value = role;
    },

    logout() {
      this.token = null;
      this.role = null;
      const tokenCookie = useCookie("token");
      const roleCookie = useCookie("role");
      tokenCookie.value = null;
      roleCookie.value = null;
    },
  },
});
