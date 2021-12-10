<template>
  <div>
    <div>
      <el-select v-model="listQuery.dormbuilding_id" placeholder="选择宿舍楼" style="width: 12%" class="filter-item" @change="fetchData">
        <el-option v-for="item in buildinglist" :key="item.id" :label="item.name" :value="item.id" />
      </el-select>
      <el-button class="upload-item" style="margin-left: 10px; width: 15%" type="primary" icon="el-icon-edit" @click="dialogImportVisible=true">
            导入
      </el-button>
    </div>
    <div v-if="dormtotal>0" class="components-container board">
      <Kanban v-for="(dorm, index) in dormlist" :key="index" :list="[{name:dorm.student1,id:1},{name:dorm.student2,id:2},{name:dorm.student3,id:3},{name:dorm.student4,id:4}]" class="kanban working" :header-text="dormlist[index].name" />
    </div>
    <el-dialog :visible.sync="dialogImportVisible" title="批量导入">
      <upload-excel-component :on-success="handleUploadSuccess" :before-upload="beforeUpload"/>
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
      ]
    }
  },
  created() {
    getBuildingList().then(response => {
      // console.log(response)
      this.listLoading = true
      this.buildinglist = response.results
      this.buildingtotal = response.count
      setTimeout(() => {
        this.listLoading = false
      }, 1.5 * 1000)
    })
    this.fetchData()
  },
  methods: {
    fetchData() {
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
      return true;
      //restricti
    },
    handleUploadSuccess({ results, header }) {
      let item
      this.uploadData = results
      this.uploadHeader = header
    },
    handleUploadConfirm(){
      importList({"list":this.uploadData,"dormbuilding_id":this.listQuery.dormbuilding_id}).then(response => {
        this.fetchData()
        this.dialogImportVisible=false
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
      //api
      // console.log(this.uploadData)
      // console.log(this.uploadHeader) 
    },
  }
}
</script>
<style lang="scss">
.board {
  width: 1000px;
  margin-left: 20px;
  display: flex;
  justify-content: space-around;
  flex-direction: row;
  align-items: flex-start;
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

