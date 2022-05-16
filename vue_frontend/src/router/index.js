import { createRouter, createWebHistory } from 'vue-router'
import { storeToRefs } from 'pinia';
import { useAuthStore } from '../stores/AuthStore';

const routes = [
  {
    path: '/',
    name: 'Feed',
    //meta data used in navigation guards to restrict access to route
    meta: {
        requiresAuth: false,
        minAccesLevel: 0
    },
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "feed" */ '../views/MainFeed.vue')
  },
  {
    path: '/profile/:uuid',
    name: 'Profile',
    meta: {
        requiresAuth: false,
        minAccesLevel: 0
    },
    component: () => import(/* webpackChunkName: "profile" */ '../views/UserProfile.vue')  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    meta: {
        requiresAuth: true,
        minAccesLevel: 200
    },
    component: () => import(/* webpackChunkName: "admin" */ '../views/AdminDashboard.vue')
  }
];

const router = createRouter({
  history: createWebHistory("/"),
  linkActiveClass: "text-blue",
  routes
});

//Navigation guards, 
//restrict acces to certain routes based on auth state and route meta data
router.beforeEach((to, from, next) => {
    //using auth store
    const authStore = useAuthStore()
    const { auth } = storeToRefs(authStore)

    //if route requires auth but user not logged in redirect to feed
    if(to.meta.requiresAuth && !auth.value) {next({ name: 'Feed' }); console.log("auth req")   }
    //if route requires auth and has ristricted acces level but the user's level is lower redirect to feed
    else if(to.meta.requiresAuth && auth.value && to.meta.minAccesLevel > auth.value.access_level) {next({ name: 'Feed' }); console.log("admin req")}  
    //else allow navigation (at this point user is logged in and has bigger or equal acces level)
    else {next(); console.log("simple next")}
})

export default router