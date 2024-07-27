import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import Assistant from '../views/Assistant.vue';

import GuessLike  from "../views/GuessLike.vue";


const routes = [
  {
    path: '/',
    name: 'home',
    // component: HomeView,
    component: GuessLike,
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  {
    path: '/register',
    name: 'register',
    component: Register
  },
  {
    path: '/Assistant',
    name: 'Assistant',
    component: Assistant,
    meta: { requiresAuth: true }
  },
  {
    path: '/GuessLike',
    name: 'GuessLike',
    component: GuessLike,
    meta: { requiresAuth: true }
  },

];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const isAuthenticated = !!localStorage.getItem('token');

  if (requiresAuth && !isAuthenticated) {
    next('/login');
  } else {
    next();
  }
});

export default router;