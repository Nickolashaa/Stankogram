import { createRouter, createWebHistory } from "vue-router"
import { useAuthStore } from "./stores/auth"

export const router = createRouter({
  routes: [
    {
      path: "/",
      component: () => import("./views/main.vue"),
      children: [
        { path: "", redirect: "/chats" },
        { path: "chats", component: () => import("./views/chats.vue") },
        { path: "profile", component: () => import("./views/profile.vue") },
        { path: "support", component: () => import("./views/support.vue") },
      ],
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

  if (!authStore.user?.is_admin && to.path === "/admin") {
    return "/"
  }
})
