<template>
    <el-form :label-position="labelPosition" class="pncop-form" label-width="160px" style="max-width: 500px">
            <el-form-item label="数据集文件：">
              <input type="file" id="csvFile" @change="handleGetFile($event)">
            </el-form-item>
            <el-form-item label="距离阈值：">
              <el-input v-model="mining_parameters.disThreshold" />
            </el-form-item>
            <el-form-item label="空间参与度阈值：">
              <el-input v-model="mining_parameters.spatialPrev" />
            </el-form-item>
            <el-form-item label="时间参与度阈值：">
              <el-input v-model="mining_parameters.temporalPrev" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="submitInfo()">计算频繁项集</el-button>
            </el-form-item>
          </el-form>
          <el-descriptions title="Pattern Results:" :column="1" border>
            <el-descriptions-item label="Positive Pattern" label-align="center" label-width="50px" align="center"
              label-class-name="my-label" class-name="my-content" width="200px">{{ result1 }}</el-descriptions-item>
            <el-descriptions-item label="Negative Pattern" label-align="center" class-name="my-content" label-width="50px" align="center">{{
              result2
            }}</el-descriptions-item>
          </el-descriptions>

          <!-- new added image part-->
          <!-- <div class="demo-image">
            <el-image v-bind:src="imageUrl" style="width: 400px; height: 100px" />
          </div> -->
          <div class="block">
            <!-- <span class="demonstration">Adjacency Graph Place</span> -->
            <el-image v-bind:src="imageUrl">
              <template #placeholder>
                <div class="image-slot">Loading<span class="dot">...</span></div>
              </template>
            </el-image>
          </div>
</template>

<script>
// import { computeFrequentSet } from './api/api.js'
// import {
//   Document,
//   Menu as IconMenu,
//   Location,
//   Setting,
// } from '@element-plus/icons-vue'
import axiosInstance from '../api/index'
import { ref } from 'vue';
const axios = axiosInstance

export default { // 组件暴露的属性
  name: 'App',
  setup() {
    // const fits = ['fill', 'contain', 'cover', 'none', 'scale-down']
    let mining_parameters = ref({
      "disThreshold": "",
      "spatialPrev": "",
      "temporalPrev": "",
      "csvFile": '',
      "csvFileName": ''
    });
    let result1 = ref('');
    let result2 = ref('');
    let imageUrl = ref('');
    function submitInfo() {
      let param = new FormData()
      param.append("disThreshold", mining_parameters.value.disThreshold)
      param.append("spatialPrev", mining_parameters.value.spatialPrev)
      param.append("temporalPrev", mining_parameters.value.temporalPrev)
      param.append("csvFile", mining_parameters.value.csvFile)
      param.append("csvFileName", mining_parameters.value.csvFileName)
      console.log(param.get("csvFile"))
      // console.log(this.mining_parameters.disThreshold)
      // console.log(this.mining_parameters.spatialPrev)
      // console.log(this.mining_parameters.temporalPrev)
      // console.log(this.mining_parameters.csvFile)
      // console.log(this.mining_parameters.csvFileName)
      axios.post('http://localhost:8000/api/pncop/', param).then(response => {
        result1.value = response.data['positiveMsg']
        result2.value = response.data['negativeMsg']
        imageUrl.value = response.data['imageUrl']
        console.log(imageUrl)
      })
    }
    function handleGetFile(e) {
      console.log("in handleGetFile function")
      mining_parameters.value.csvFile = e.target.files[0]
      mining_parameters.value.csvFileName = e.target.files[0].name
    }
    return { mining_parameters, result1, result2, imageUrl, submitInfo, handleGetFile }
  },
  // data() {
  //   return {
  //     msg: 'Welcome to Your Vue.js App',
  //     mining_parameters: {
  //       "disThreshold": "",
  //       "spatialPrev": "",
  //       "temporalPrev": "",
  //       "csvFile":'',
  //       "csvFileName":''
  //     },
  //     result1: '',
  //     result2: ''
  //   }
  // },

  // methods: {
  //   submitInfo() {
  //     let param = new FormData()
  //     param.append("disThreshold", this.mining_parameters.disThreshold)
  //     param.append("spatialPrev", this.mining_parameters.spatialPrev)
  //     param.append("temporalPrev", this.mining_parameters.temporalPrev)
  //     param.append("csvFile", this.mining_parameters.csvFile)
  //     param.append("csvFileName", this.mining_parameters.csvFileName)
  //     console.log(param.get("csvFile"))
  //     // console.log(this.mining_parameters.disThreshold)
  //     // console.log(this.mining_parameters.spatialPrev)
  //     // console.log(this.mining_parameters.temporalPrev)
  //     // console.log(this.mining_parameters.csvFile)
  //     // console.log(this.mining_parameters.csvFileName)
  //     axios.post('http://localhost:8000/api/pncop/', param).then(response => {
  //       this.result1 = response.data['positiveMsg']
  //       this.result2 = response.data['negativeMsg']
  //     })
  //   },
  //   handleGetFile(e) {
  //     console.log("in handleGetFile function")
  //     this.mining_parameters.csvFile = e.target.files[0]
  //     this.mining_parameters.csvFileName = e.target.files[0].name
  //   }
  // }
}
</script>

<style scoped>
.my-label {
  background: var(--el-color-success-light-9);
}

.my-content {
  background: var(--el-color-danger-light-9);
}

/* image part */
.demo-image__placeholder .block {
  padding: 30px 0;
  text-align: center;
  border-right: solid 1px var(--el-border-color);
  display: inline-block;
  width: 49%;
  box-sizing: border-box;
  vertical-align: top;
}
.demo-image__placeholder .demonstration {
  display: block;
  color: var(--el-text-color-secondary);
  font-size: 14px;
  margin-bottom: 20px;
}
.demo-image__placeholder .el-image {
  padding: 0 5px;
  max-width: 300px;
  max-height: 200px;
}

.demo-image__placeholder.image-slot {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  background: var(--el-fill-color-light);
  color: var(--el-text-color-secondary);
  font-size: 14px;
}
.demo-image__placeholder .dot {
  animation: dot 2s infinite steps(3, start);
  overflow: hidden;
}

/* .el-menu {
  background-color: #d3dce6;
} */
</style>
