<template>
  <el-container>
    <el-header>
      <h1>Spatio-Temporal Data Mining</h1>
    </el-header>
    <el-container>
      <el-aside>
        <el-menu router default-active="/pncop">
          <el-menu-item index="/">
            <span>PNCOP Algorithm</span>
          </el-menu-item>
          <el-menu-item index="pacop">
            <span>PACOP Algorithm</span>
          </el-menu-item>
          <el-menu-item index="pncor">
            <span>Traditional PNCOR Algorithm</span>
          </el-menu-item>
          <el-menu-item index="fastpncop">
            <span>Fast PNCOP Algorithm</span>
          </el-menu-item>
          <el-menu-item index="joinbased">
            <span>Join-based Algorithm</span>
          </el-menu-item>
          <el-menu-item index="joinless">
            <span>Joinless Algorithm</span>
          </el-menu-item>
          <el-menu-item index="regional">
            <span>Regional Algorithm</span>
          </el-menu-item>
          <el-menu-item index="weighted">
            <span>Weighted Algorithm</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-main>
          <router-view/>
        </el-main>
        <el-footer>
          <h5>Ecust 2023 @copyright</h5>
        </el-footer>
      </el-container>
    </el-container>
  </el-container>
</template>

<script>

</script>

<style scoped>
.el-container {
  height: 100%;
}

.el-header {
  background-color: #D4D7DE;
  color: #303133;
  text-align: left;
  line-height: 50px;
  height: 10vh;
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
  height: 82vh;
  /* height: 10px */
}

/* .el-menu {
  background-color: #d3dce6;
} */
</style>
