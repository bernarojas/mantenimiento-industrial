import Vue from 'vue'
import VueResource from 'vue-resource'
import ListarBook from './ComponenteFoto/ListarBook'
import lodash from 'lodash'

Vue.use(VueResource, lodash)

new Vue(ListarBook).$mount(".listarBook")