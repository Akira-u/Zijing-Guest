<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input v-model="guest_name" placeholder="访客姓名" style="width: 25%;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-input v-model="listQuery.student_id__icontains" placeholder="学号" style="width: 25%" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-select v-model="listQuery.is_student" placeholder="选择身份" style="width: 10%" class="filter-item" @change="handleFilter">
            <el-option v-for="item in typeOptions" :key="item.key" :label="item.label" :value="item.key" />
      </el-select>
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        查找
      </el-button>
        <el-checkbox v-model="fuzzySearch" class="filter-item" style="margin-left:15px;">
        姓名模糊查找
      </el-checkbox>
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="clearFilter">
        清除当前查找条件
      </el-button>
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleBlackList">
        加入黑名单
      </el-button>
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleWhiteList">
        加入白名单
      </el-button>
    </div>

    <el-table
      v-loading="listLoading"
      :data="list"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" align="center" />
      <el-table-column align="center" label="ID" width="95">
        <template slot-scope="scope">
          {{ scope.$index }}
        </template>
      </el-table-column>
      <el-table-column label="姓名">
        <template slot-scope="scope">
          {{ scope.row.name }}
          <el-tag :type="scope.row.is_student | tagFilter">{{scope.row.is_student | typeFilter}}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="信用状态" width="110" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.credit | tagFilter">{{scope.row.credit | creditFilter}}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="学号" width="110" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.student_id | stuidFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column label="手机号" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.phone | phoneFilter}}
        </template>
      </el-table-column>
      <!-- <el-table-column class-name="status-col" label="Status" width="110" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.status | statusFilter">{{ scope.row.status }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column align="center" prop="created_at" label="Display_time" width="200">
        <template slot-scope="scope">
          <i class="el-icon-time" />
          <span>{{ scope.row.display_time }}</span>
        </template>
      </el-table-column> -->
    </el-table>
    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync=limit @pagination="fetchData" />

  </div>
</template>

<script>
import { getList, toBlackList, toWhiteList } from '@/api/guest'
import waves from '@/directive/waves'
import Pagination from '@/components/Pagination'

export default {
  components :{ Pagination },
  directives: { waves },
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'gray',
        deleted: 'danger'
      }
      return statusMap[status]
    },
    typeFilter(type) {
        if (type)return "学生"
        else return "其他访客"
    },
    tagFilter(type) {
        if (type)return "success"
        else return  "danger"
    },
    creditFilter(credit){
        if (credit)return "白名单"
        else return "黑名单"
    },
    stuidFilter(student_id){
        // console.log(student_id)
        if(student_id===null)return "其他访客无学号"
        else return student_id
    },
    phoneFilter(phone){
        if(phone===null)return "该访客还未录入手机号"
        else return phone
    }
  },
  data() {
    return {
      list: null,
      listLoading: true,
      listQuery: {
        page: 1,
        student_id: undefined,
        student_id__icontains: undefined,
        name: undefined,
        icontains: undefined,
        is_student: undefined,
        // ordering: 'id'
      },
      guest_name: undefined,
      fuzzySearch: false,
      multipleSelection:[],
      total:0,
      limit:0,
      typeOptions: [{ label: '学生', key: 'true' }, { label: '其他访客', key: 'false' }],
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.listLoading = true
      console.log('fetchData')
      getList(this.listQuery).then(response => {
        console.log(response)
        this.list = response.results
        this.total = response.count
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      if (this.fuzzySearch) {
        this.listQuery.name__icontains = this.guest_name
        this.listQuery.name = undefined
      } else {
        this.listQuery.name__icontains = undefined
        this.listQuery.name = this.guest_name
      }
      this.fetchData()
    },
    clearFilter() {
      this.listQuery= {
        page: 1,
        student_id: undefined,
        student_id__icontains: undefined,
        name: undefined,
        icontains: undefined,
        is_student: undefined,
      },
      this.fetchData()
    },
    handleSelectionChange(val){
        // console.log(val)
        this.multipleSelection =val
    },
    handleBlackList(){
      console.log(this.multipleSelection)
      toBlackList(this.multipleSelection).then(()=>{
        this.fetchData()
      })
    },
    handleWhiteList(){
      toWhiteList(this.multipleSelection).then(()=>{
        this.fetchData()
      })
    },
  }
}
</script>
