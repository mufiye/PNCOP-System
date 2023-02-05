<template>
  <el-container>
    <el-header>
      <h1>Spatio-Temporal Data Mining</h1>
    </el-header>
    <el-container>
      <el-aside>
        <el-menu>
          <el-menu-item index="1">
            <!-- <el-icon><icon-menu /></el-icon> -->
            <span>PNCOP Algorithm</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-main>
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
            <el-descriptions-item label="Negative Pattern" label-align="center" label-width="50px" align="center">{{
              result2
            }}</el-descriptions-item>
          </el-descriptions>
        </el-main>
        <el-footer>
          <h5>Ecust 2023 @copyright</h5>
        </el-footer>
      </el-container>
    </el-container>
  </el-container>
</template>

<script>
// import { computeFrequentSet } from './api/api.js'
// import {
//   Document,
//   Menu as IconMenu,
//   Location,
//   Setting,
// } from '@element-plus/icons-vue'
import axiosInstance from './api/index'
import { ref } from 'vue';
const axios = axiosInstance

export default { // 组件暴露的属性
  name: 'App',
  setup() {
    let mining_parameters = ref({
      "disThreshold": "",
      "spatialPrev": "",
      "temporalPrev": "",
      "csvFile": '',
      "csvFileName": ''
    });
    let result1 = ref('');
    let result2 = ref('');
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
      })
    }
    function handleGetFile(e) {
      console.log("in handleGetFile function")
      mining_parameters.value.csvFile = e.target.files[0]
      mining_parameters.value.csvFileName = e.target.files[0].name
    }
    return { mining_parameters, result1, result2, submitInfo, handleGetFile }
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

.el-container {
  height: 100%;
}

.el-header {
  background-color: #D4D7DE;
  color: #303133;
  text-align: left;
  line-height: 50px;
  height: 100px;
}

.el-footer {
  background-color: #D4D7DE;
  color: #303133;
  text-align: right;
  line-height: 50px;
}

.el-aside {
  background-color: #E6E8EB;
  color: #303133;
  text-align: center;
  line-height: 200px;
  width: 300px;
}

.el-main {
  background-color: #FFFFFF;
  color: #303133;
  text-align: center;
  line-height: 160px;
  height: 710px;
}

/* .el-menu {
  background-color: #d3dce6;
} */
</style>
