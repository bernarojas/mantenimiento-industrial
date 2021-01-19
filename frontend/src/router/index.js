import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '../components/HelloWorld'

import ListarBook from '../components/ComponenteFoto/ListarBook'
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/books',
      name: 'ListBook',
      component: ListarBook
    },
  ],
  mode: 'history'
})
