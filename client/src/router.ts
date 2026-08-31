import { createRouter, createWebHistory } from "vue-router"
import { useAuthStore } from "./stores/auth"

export const router = createRouter({
  routes: [
    {
      path: "/",
      component: () => import("./views/main.vue"),
      children: [
        { path: "", redirect: "/home" },
        { path: "home", component: () => import("./views/home.vue") },
        { path: "chats/:chatId?", component: () => import("./views/chats.vue") },
        { path: "users", component: () => import("./views/users.vue") },
        { path: "support", component: () => import("./views/support.vue") },
        {
          path: "admin",
          component: () => import("./views/admin.vue"),
          meta: { requiresAdmin: true },
          children: [
            { path: "", redirect: "/admin/users" },
            { path: "users", component: () => import("./views/admin-users.vue") },
            { path: "chats/:chatId?", component: () => import("./views/admin-chats.vue") },
            {
              path: "notifications",
              component: () => import("./views/admin-notifications.vue"),
            },
          ],
        },
      ],
    },
    {
      path: "/auth",
      component: () => import("./views/auth.vue"),
    },
    {
      path: "/reset-password-confirm",
      component: () => import("./views/reset-password-confirm.vue"),
    },
  ],
  history: createWebHistory(),
})

export const PUBLIC_PATHS = ["/auth", "/reset-password-confirm"]

router.beforeEach((to) => {
  const authStore = useAuthStore()

  if (!authStore.accessToken && !PUBLIC_PATHS.includes(to.path)) {
    return "/auth"
  }

  if (authStore.accessToken && to.path === "/auth") {
    return "/"
  }

  if (to.matched.some((record) => record.meta.requiresAdmin) && !authStore.user?.isAdmin) {
    return "/"
  }
})
