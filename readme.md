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
# 项目特点
该系统主要用于挖掘时空同位模式，并且对时空数据以及挖掘出来的模式进行展示。该系统支持多种时空同位数据挖掘算法，如我们提出的PNCOP、Fast-PNCOP,以及用于对照的PACOP。用户可以在操作界面上上传需要挖掘的数据集，定义好距离阈值、时间支持度和空间支持度，之后点击让系统进行挖掘，得益于我们高效的算法和系统，很快界面上就会展示出挖掘得到的模式以及对于时空数据的可视化结果。通过左侧的导航栏可以切换不同的算法进行更多的时空同位挖掘尝试。
该系统使用前后端分离的架构，前端使用vue、vue-router、element-plus框架，后端使用了django框架。Vue作为轻量级的框架，其支持双向数据绑定、组件化，这允许我们将一个页面拆分为多个组件进行高效地开发，同时vue-router支持在单页面中进行组件的路由切换，这满足了我们在页面中嵌入多个算法模块并进行切换。而element-plus作为最适配vue的样式库，其提供了丰富的样式供我们填充、美化页面。在后端，我们使用了django框架，它是基于python的web框架，可拓展性强且基于模型-视图-控制器的软件架构模式，使得后端的开发更加模块化且易于维护，并且天然地适配我们的算法层。


