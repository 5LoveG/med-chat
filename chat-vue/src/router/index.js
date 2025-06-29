
import Vue from 'vue'
import VueRouter from 'vue-router'
import ChatView from '../views/ChatView.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/chat',
    name: 'chat',
    component: ChatView
  },

  {
    path: '/about',
    name: 'about',

    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/picture',
    name: 'picture',

    component: () => import(/* webpackChunkName: "about" */ '../views/PictureView.vue')
  }
]

const router = new VueRouter({
  routes
})

export default router
