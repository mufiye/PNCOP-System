<template>
  <div class="app">
    <h1>{{ msg }}</h1>
    <!-- form to add a book -->
    <form action="">
      <!--文件框, 对应的数据集, 上传数据集-->
      数据集文件：<input type="file" id="csvFile" @change="handleGetFile($event)"><br>
      距离阈值：<input type="text" placeholder="请输入距离阈值" v-model="mining_parameters.disThreshold"><br>
      空间参与度阈值：<input type="text" placeholder="请输入空间参与度阈值" v-model="mining_parameters.spatialPrev"><br>
      时间参与度阈值：<input type="text" placeholder="请输入时间参与度阈值" v-model="mining_parameters.temporalPrev">
    </form>
    <el-button type="primary" @click="submitInfo()">计算频繁项集</el-button>
    <p>Positive Set: {{ result1 }}</p>
    <p>Negative Set: {{ result2 }}</p>
  </div>
</template>

<script>
// import { computeFrequentSet } from './api/api.js'
import axiosInstance from './api/index'
const axios = axiosInstance

export default { // 组件暴露的属性
  name: 'App',
  data() {
    return {
      msg: 'Welcome to Your Vue.js App',
      mining_parameters: {
        "disThreshold": "",
        "spatialPrev": "",
        "temporalPrev": "",
        "csvFile":'',
        "csvFileName":''
      },
      result1: '',
      result2: ''
    }
  },
  methods: {
    submitInfo() {
      let param = new FormData()
      param.append("disThreshold", this.mining_parameters.disThreshold)
      param.append("spatialPrev", this.mining_parameters.spatialPrev)
      param.append("temporalPrev", this.mining_parameters.temporalPrev)
      param.append("csvFile", this.mining_parameters.csvFile)
      param.append("csvFileName", this.mining_parameters.csvFileName)
      console.log(param.get("csvFile"))
      // console.log(this.mining_parameters.disThreshold)
      // console.log(this.mining_parameters.spatialPrev)
      // console.log(this.mining_parameters.temporalPrev)
      // console.log(this.mining_parameters.csvFile)
      // console.log(this.mining_parameters.csvFileName)
      axios.post('http://localhost:8000/api/pncop/', param).then(response => {
        this.result1 = response.data['positiveMsg']
        this.result2 = response.data['negativeMsg']
      })
    },
    handleGetFile(e) {
      console.log("in handleGetFile function")
      this.mining_parameters.csvFile = e.target.files[0]
      this.mining_parameters.csvFileName = e.target.files[0].name
    }
  }
  // created: function () {

  // }
}
</script>

<style>

</style>
