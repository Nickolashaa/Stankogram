import { createRouter, createWebHistory } from "vue-router"
import { useAuthStore } from "./stores/auth"

export const router = createRouter({
  routes: [
    {
      path: "/",
      component: () => import("./views/main.vue"),
    },
    {
      path: "/auth",
      component: () => import("./views/auth.vue"),
    },
  ],
  history: createWebHistory(),
})

router.beforeEach((to) => {
  const authStore = useAuthStore()

  if (!authStore.accessToken && to.path !== "/auth") {
    return "/auth"
  }

  if (authStore.accessToken && to.path === "/auth") {
    return "/"
  }
})
