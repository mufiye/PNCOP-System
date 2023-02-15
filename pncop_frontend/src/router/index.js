import {createRouter, createWebHashHistory} from 'vue-router'

// 1. 定义路由组件
import Pncop from "../components/Pncop.vue"
import Pacop from "../components/Pacop.vue"

// 2. 定义一些路由
const routes = [
    {path: '/', component: Pncop}, 
    {path: '/pacop', component: Pacop},
]

// 3.创建路由实例并传递routes配置
const router = createRouter({
    history: createWebHashHistory(),
    routes
})

export default router