import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
// import { Picture as IconPicture } from '@element-plus/icons-vue'

import App from './App.vue'
import router from './router'

let app = createApp(App)
// app.component(IconPicture, IconPicture);
// for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
//     app.component(key, component)
// }
app.use(ElementPlus)
app.use(router)
app.mount('#app')


