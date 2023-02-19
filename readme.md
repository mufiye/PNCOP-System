# 系统设计
## 前端
* 上边栏：导航栏（一些信息）
* 左侧栏：选择不同的算法
* 右边栏：
    * 文件上传框
    * 设置距离阈值
    * 设置空间阈值
    * 设置时间阈值
    * 计算频繁项集
    * 结果展示框
* 下边栏：信息栏（一些其余信息）
## 后端
* 读取文件，距离阈值、空间阈值、时间阈值
* 将参数输入算法进行计算得到频繁项集
* 输出频繁项集到前端
* (如果可能就输出一幅图像)
# Dependency
## 前端
* npm(包管理工具): 8.19.2
* vue: 3.2.45
* vue-router: 4.1.6
* element-plus: 2.2.29
## 后端
* django: 4.1.3
* pandas: 1.4.4
## Some docs to install dependency
* [npm install](https://positiwise.com/blog/how-to-install-npm-and-node-js-on-mac-and-windows/)，maybe it works
* 简单来说就是`npm install vue`，[vue install](https://v2.cn.vuejs.org/v2/guide/installation.html)
* 可以不安装，debug用的[vue dev tools](https://devtools.vuejs.org/guide/installation.html)
* 简单来说就是`npm install element-plus --save`，[element-plus](https://element-plus.org/en-US/guide/installation.html#using-package-manager)
* 简单来说就是`npm install vue-router@4`，[vue-router](https://router.vuejs.org/zh/installation.html)
* [django install](https://docs.djangoproject.com/en/4.1/intro/install/)
# How to run
## 前端
```shell
cd /path/to/PNCOP_sys/pncop_frontend
npm run serve
```
## 后端
```shell
cd /path/to/PNCOP_sys/pncop_backend
python manage.py runserver
```


