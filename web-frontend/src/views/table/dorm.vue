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
          <el-button class="upload-item" type="primary" icon="el-icon-upload2" @click="dialogImportVisible=true">
            导入Excel
          </el-button>
        </el-col>
        <el-col :span="6">
          <el-button :loading="downloadLoading" type="primary" icon="el-icon-document" @click="handleDownload">
            导出Excel
          </el-button>
        </el-col>
        <el-col :span="6">
          <el-button :loading="downloadLoading" type="primary" icon="el-icon-download" @click="handleDownloadModel">
            下载Excel模板
          </el-button>
        </el-col>
      </el-row>
    </div>
    <div v-if="dormtotal>0" class="board">
      <Kanban v-for="(dorm, index) in dormlist_show" :key="index" :list="[{name:dorm.student1,id:1},{name:dorm.student2,id:2},{name:dorm.student3,id:3},{name:dorm.student4,id:4}]" class="kanban todo" :header-text="dormlist[index].name" />
    </div>
    <el-dialog :visible.sync="dialogImportVisible" title="批量导入">
      <upload-excel-component :on-success="handleUploadSuccess" :before-upload="beforeUpload" />
      <el-table :data="uploadData" stripe border highlight-current-row style="width: 100%;margin: 20px auto;">
        <el-table-column v-for="(item, index) of uploadHeader" :key="item" :prop="item" :label="uploadHeader_show[index]" />
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
      dormlist_show: [],
      buildingtotal: 0,
      dormtotal: 0,
      listLoading: false,
      dialogImportVisible: false,
      uploadData: [],
      uploadHeader: ['name', 'student1', 'student2', 'student3', 'student4'],
      uploadHeader_show: ['宿舍号', '1号床', '2号床', '3号床', '4号床'],
      listQuery: {
        dormbuilding_id: 1
      },
      downloadLoading: false,
      modellist: [
        {
          name: '101A',
          student1: '张三',
          student2: '李四',
          student3: '王五',
          student4: '刘六'
        },
        {
          name: '101B',
          student1: '羞男',
          student2: '宁',
          student3: '明',
          student4: '杰克辣舞'
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
        this.dormlist_show=[...this.dormlist] // deep copy
        // translate 'empty' to '空'
        this.dormlist_show.forEach(dorm=>{
          for(const i in dorm){
            if(dorm[i]==='empty'){
              dorm[i]='空'
            }
          }
        })
        this.dormtotal = response.count
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    },
    beforeUpload(file) {
      // verify file format
      const filename = file.name
      if (!filename || !(filename.endsWith('.xlsx') || filename.endsWith('.xls'))) {
        this.$message({ type: 'error', message: '仅支持.xlsx或.xls格式的文件！' })
        return false
      }
      return true
    },
    handleUploadSuccess({ results, header }) {
      for (const i in results) {
        // format results: filter redundant column
        results[i] = (({ name, student1, student2, student3, student4 }) => ({ name, student1, student2, student3, student4 }))(results[i])
        console.log(results)
        // fill missing column
        const format = {
          name: '未指定宿舍号',
          student1: '无',
          student2: '无',
          student3: '无',
          student4: '无'
        }
        results[i] = Object.assign(format, results[i])
      }
      this.uploadData = results
    },
    handleUploadConfirm() {
      importList({ 'list': this.uploadData, 'dormbuilding_id': this.listQuery.dormbuilding_id }).then(response => {
        this.fetchData()
        this.dialogImportVisible = false
      })
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

