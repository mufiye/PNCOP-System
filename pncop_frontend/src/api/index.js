// import Vue from 'vue'
import Axios from 'axios'

const axiosInstance = Axios.create({
    withCredentials: true
})

// 使用拦截器处理csrf问题
// axiosInstance.interceptors.request.use((config) => {
//     // config.headers['X-Requested-With'] = 'XMLHttpRequest';
//     // let regex = /.*csrftoken=([^;.]*).*$/; // 用于从cookie中匹配 csrftoken值
//     // config.headers['X-CSRFToken'] = document.cookie.match(regex) === null ? null : document.cookie.match(regex)[1];
//     return config
// });


axiosInstance.interceptors.response.use(
    response => {
        return response
    },
    error => {
        return Promise.reject(error)
    }
)


// Vue.prototype.axios = axiosInstance

export default axiosInstance