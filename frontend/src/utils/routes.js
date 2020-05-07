import Hello from '../pages/Hi.vue'
import Bye from '../pages/Bi.vue'
import Login from '../pages/Login.vue'

const routes = [
  {path: '/login', name: 'login', component: Login},
  {path: '/hello', name: 'hello', component: Hello},
  {path: '/bye', name: 'bye', component: Bye},
  {path: '', name:'default'}
]

export default  {
  routes
}
