<template>
  <div>
    <div style="margin-top: 20px">
      <el-row>
        <el-col :span="6">
          <el-select v-model="listQuery.dormbuilding_id" placeholder="选择宿舍楼" style="margin-left: 20px" class="filter-item" @change="fetchData">
            <el-option v-for="item in buildinglist" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-button class="upload-item" style="margin-left: 10px" type="primary" icon="el-icon-upload2" @click="dialogImportVisible=true">
            导入Excel
          </el-button>
        </el-col>
        <el-col :span="6">
          <el-button :loading="downloadLoading" style="margin:0 0 20px 20px;" type="primary" icon="el-icon-document" @click="handleDownload">
            导出Excel
          </el-button>
        </el-col>
        <el-col :span="6">
          <el-button :loading="downloadLoading" style="margin:0 0 20px 20px;" type="primary" icon="el-icon-download" @click="handleDownloadModel">
            下载Excel模板
          </el-button>
        </el-col>
      </el-row>
    </div>
    <div v-if="dormtotal>0" class="board">
      <Kanban v-for="(dorm, index) in dormlist" :key="index" :list="[{name:dorm.student1,id:1},{name:dorm.student2,id:2},{name:dorm.student3,id:3},{name:dorm.student4,id:4}]" class="kanban todo" :header-text="dormlist[index].name" />
    </div>
    <el-dialog :visible.sync="dialogImportVisible" title="批量导入">
      <upload-excel-component :on-success="handleUploadSuccess" :before-upload="beforeUpload" />
      <el-table :data="uploadData" border highlight-current-row style="width: 100%;margin-top:20px;">
        <el-table-column v-for="item of uploadHeader" :key="item" :prop="item" :label="item" />
      </el-table>
      <el-button type="danger" @click="dialogImportVisible=false">取消</el-button>
      <el-button type="primary" @click="handleUploadConfirm()">确定</el-button>
    </el-dialog>

  </div>
</template>
<script>
import { getBuildingList, getDormList, importList } from '@/api/dorm'
import Kanban from '@/components/Kanban'
import UploadExcelComponent from '@/components/UploadExcel/index.vue'

export default {
  components: {
    Kanban,
    UploadExcelComponent
  },
  data() {
    return {
      dormbuilding: '紫荆一号楼',
      buildinglist: [],
      dormlist: [],
      buildingtotal: 0,
      dormtotal: 0,
      listLoading: false,
      group: 'mission',
      dialogImportVisible: false,
      uploadData: [],
      uploadHeader: [],
      listQuery: {
        dormbuilding_id: 1
      },
      list1: [
        { name: 'Mission', id: 1 },
        { name: 'Mission', id: 2 },
        { name: 'Mission', id: 3 },
        { name: 'Mission', id: 4 }
      ],
      list2: [
        { name: 'Mission', id: 5 },
        { name: 'Mission', id: 6 },
        { name: 'Mission', id: 7 }
      ],
      list3: [
        { name: 'Mission', id: 8 },
        { name: 'Mission', id: 9 },
        { name: 'Mission', id: 10 }
      ],
      downloadLoading: false,
      modellist: [
        {
          name: '101A',
          student1: '张三',
          student2: '李四',
          student3: '王五',
          student4: '刘六'
        }
      ]
    }
  },
  created() {
    getBuildingList().then(response => {
      // console.log(response)
      this.listLoading = true
      this.buildinglist = response.results
      this.buildingtotal = response.count
      console.log('buildinglist:', this.buildinglist)
      setTimeout(() => {
        this.listLoading = false
      }, 1.5 * 1000)
    })
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.buildinglist.forEach(item => {
        if (item.id === this.listQuery.dormbuilding_id) {
          this.dormbuilding = item.name
          return
        }
      })
      this.listLoading = true
      getDormList(this.listQuery).then(response => {
        this.dormlist = response.results
        this.dormtotal = response.count
        // console.log(this.dormlist)
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    },
    beforeUpload(file) {
      return true
      // restricti
    },
    handleUploadSuccess({ results, header }) {
      this.uploadData = results
      this.uploadHeader = header
    },
    handleUploadConfirm() {
      importList({ 'list': this.uploadData, 'dormbuilding_id': this.listQuery.dormbuilding_id }).then(response => {
        this.fetchData()
        this.dialogImportVisible = false
      })
      // this.$api.person.person_import({"results":this.uploadData,"header":this.uploadHeader}).then(response=>{
      //   let result = response.data.result
      //   if (result=='success'){
      //     this.dialogImportVisible=false
      //   }
      //   else{
      //     this.$notify({
      //       title: 'Fail',
      //       message: result,
      //       type: 'fail',
      //       duration: 2000
      //     })
      //   }
      //   this.fetchData()
      // })
      // api
      // console.log(this.uploadData)
      // console.log(this.uploadHeader)
    },
    handleDownload() {
      this.downloadLoading = true
      import('@/vendor/Export2Excel').then(excel => {
        const tHeader = ['name', 'student1', 'student2', 'student3', 'student4']
        const filterVal = ['name', 'student1', 'student2', 'student3', 'student4']
        const list = this.dormlist
        const data = this.formatJson(filterVal, list)
        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: this.dormbuilding + '名单'
        })
        this.downloadLoading = false
      })
    },
    handleDownloadModel() {
      this.downloadLoading = true
      import('@/vendor/Export2Excel').then(excel => {
        const tHeader = ['name', 'student1', 'student2', 'student3', 'student4']
        const filterVal = ['name', 'student1', 'student2', 'student3', 'student4']
        const list = this.modellist
        const data = this.formatJson(filterVal, list)
        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: '名单模板'
        })
        this.downloadLoading = false
      })
    },
    formatJson(filterVal, jsonData) {
      return jsonData.map(v => filterVal.map(j => {
        return v[j]
      }))
    }
  }
}
</script>
<style lang="scss">
.board {
  width: 100%;
  margin-left: 20px;
  margin-top: 20px;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  row-gap: 20px;
  column-gap: 20px;
}
.kanban {
  &.todo {
    .board-column-header {
      background: #4A9FF9;
    }
  }
  &.working {
    .board-column-header {
      background: #f9944a;
    }
  }
  &.done {
    .board-column-header {
      background: #2ac06d;
    }
  }
}
</style>

