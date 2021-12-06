<template>
  <div class="sidebar">
    <el-row class="tac">
      <el-col :span="25">
        <h1></h1>
        <el-radio-group
          v-model="isCollapse"
          size="small"
          style="margin-bottom: 20px;margin-left:10px"
        >
          <el-radio-button icon="el-icon-arrow-left" :label="false"
            ><i class="el-icon-s-unfold"></i
          ></el-radio-button>
          <el-radio-button :label="true"
            ><i class="el-icon-s-fold"></i
          ></el-radio-button>
        </el-radio-group>
        <el-menu
          default-active="this.show"
          class="el-menu-vertical-demo"
          :router="false"
          :collapse="isCollapse"
          @open="handleOpen"
          @close="handleClose"
          @select="handleSelect"
          :unique-opened="true"
        >
            <el-submenu index="data">
              <template slot="title">
                <i class="el-icon-s-data"></i>
                <span>数据管理</span>
              </template>
              <el-menu-item index="/project/DatasourceList">
                <i class="el-icon-paperclip"></i>
                <span slot="title">数据源管理</span>
              </el-menu-item>
              <el-menu-item index="/project/DatasetList">
                <i class="el-icon-document"></i>
                <span slot="title">数据集管理</span>
              </el-menu-item>
                        <el-menu-item index="/project/DataNoteList">
                <i class="el-icon-document"></i>
                <span slot="title">标注集管理</span>
              </el-menu-item>
            </el-submenu>


<!--            <el-menu-item index="/project/FileList">-->
<!--                <i class="el-icon-folder-opened"></i>-->
<!--                <span slot="title">文件管理</span>-->
<!--            </el-menu-item>-->
            <el-submenu index="filesystem">
              <template slot="title">
                <i class="el-icon-folder"></i>
                <span>文件管理</span>
              </template>
              <el-menu-item index="/project/OpFileList">
                <i class="el-icon-folder-opened"></i>
                <span slot="title">算子文件管理</span>
              </el-menu-item>
              <el-menu-item index="/project/LocalFileList">
                <i class="el-icon-folder-opened"></i>
                <span slot="title">本地文件管理</span>
              </el-menu-item>
              <el-menu-item index="/project/HDFSFileList">
                <i class="el-icon-folder-opened"></i>
                <span slot="title">HDFS文件管理</span>
              </el-menu-item>
              <el-menu-item index="/project/TrainFileList">
                <i class="el-icon-folder-opened"></i>
                <span slot="title">训练相关文件管理</span>
              </el-menu-item>
            </el-submenu>


            <el-menu-item index="/project/OperatorList">
              <i class="el-icon-suitcase"></i>
              <span slot="title">算子管理</span>
            </el-menu-item>
            <el-submenu index="workflow">
              <template slot="title">
                <i class="el-icon-s-marketing"></i>
                <span>工作流管理</span>
              </template>
              <el-menu-item index="/project/WorkflowList">
                <i class="el-icon-s-grid"></i>
                <span slot="title">工作流模板管理</span>
              </el-menu-item>
              <el-menu-item index="/project/ConfigList">
                <i class="el-icon-set-up"></i>
                <span slot="title">工作流配置管理</span>
              </el-menu-item>
              <el-menu-item index="/project/ApplicationList">
                <i class="el-icon-receiving"></i>
                <span slot="title">工作流实例管理</span>
              </el-menu-item>
            </el-submenu>
        <el-submenu index="env">
              <template slot="title">
                <i class="el-icon-s-help"></i>
                <span>环境管理</span>
              </template>
          <el-menu-item index="/project/DataEnvList">
            <i class="el-icon-folder"></i>
            <span slot="title">存储环境管理</span>
          </el-menu-item>

          <!-- <el-menu-item index="EnvironmentList">
            <i class="el-icon-s-promotion"></i>
            <span slot="title">环境管理</span>
          </el-menu-item> -->

          <el-menu-item index="/project/RunEnvTypeList">
            <i class="el-icon-lollipop"></i>
            <span slot="title">计算环境管理</span>
          </el-menu-item>
        </el-submenu>

         <el-submenu index="model">
              <template slot="title">
                <i class="el-icon-folder-opened"></i>
                <span slot="title">模型管理</span>
              </template>
          <el-menu-item index="/project/ModelList">
            <i class="el-icon-folder"></i>
            <span slot="title">学习模型管理</span>
          </el-menu-item>

          <el-menu-item index="/project/ServiceList">
            <i class="el-icon-lollipop"></i>
            <span slot="title">服务实例管理</span>
          </el-menu-item>
        </el-submenu>
          <el-submenu index="organization">
            <template slot="title">
              <i class="el-icon-menu"></i>
              <span>组织结构</span>
            </template>
            <el-menu-item index="/project/OrganizationList">
              <i class="el-icon-share"></i>
              <span slot="title">组织维护</span>
            </el-menu-item>
            <el-menu-item index="/project/PersonList">
              <i class="el-icon-user"></i>
              <span slot="title">人员维护</span>
            </el-menu-item>
            <el-menu-item index="/project/CharacterList">
              <i class="el-icon-user-solid"></i>
              <span slot="title">角色维护</span>
            </el-menu-item>
            <el-menu-item index="/project/GroupList">
              <i class="el-icon-ship"></i>
              <span slot="title">工作组维护</span>
            </el-menu-item>
          </el-submenu>
        </el-menu>
      </el-col>
    </el-row>
  </div>
</template>

<style lang="scss">
.el-menu-vertical-demo {
  height: 600px;
}
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
  height: 600px;
  min-width: 150px;
}
</style>

<script>
export default {
  name: "Sidebar",
  data() {
    return {
      isCollapse: true
    };
  },
  watch:{
    isCollapse(newVal){
      this.$emit('getCollaspe', newVal)
    }
  },
  methods: {
    handleSelect(index,indexPath){
      this.$router.push({
        path: index,
        query: {token: this.$route.query.token,single: this.$route.query.single}
      })
    },
    handleOpen(key, keyPath) {
      // console.log(key, keyPath);
    },
    handleClose(key, keyPath) {
      // console.log(key, keyPath);
    }
  }
};
</script>
