import {createRouter, createWebHashHistory} from 'vue-router'

// 1. 定义路由组件
import Pncop from "../components/Pncop.vue"
import Pacop from "../components/Pacop.vue"
import Joinbased from "../components/Joinbased.vue"
import Regional from "../components/Regional.vue"
import Weighted from "../components/Weighted.vue"

// 2. 定义一些路由
const routes = [
    {path: '/', component: Pncop}, 
    {path: '/pacop', component: Pacop},
    {path: '/pncor', component: Pncop},
    {path: '/fastpncop', component: Pncop},
    {path: '/joinbased', component: Joinbased},
    {path: '/joinless', component: Joinbased},
    {path: '/regional', component: Regional},
    {path: '/weighted', component: Weighted}
]

// 3.创建路由实例并传递routes配置
const router = createRouter({
    history: createWebHashHistory(),
    routes
})

export default router