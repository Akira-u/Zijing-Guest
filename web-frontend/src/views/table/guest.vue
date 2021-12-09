<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input v-if="fuzzySearch==false" v-model="listQuery.name" placeholder="访客姓名" style="width: 150px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-input v-if="fuzzySearch==true" v-model="listQuery.name__icontains" placeholder="访客姓名（模糊）" style="width: 150px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-input v-model="listQuery.student_id" placeholder="学号" style="width: 110px" class="filter-item" @keyup.enter.native="handleFilter" />

      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        查找
      </el-button>
        <el-checkbox v-model="fuzzySearch" class="filter-item" style="margin-left:15px;">
        姓名模糊查找
      </el-checkbox>
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="clearFilter">
        清除当前查找条件
      </el-button>
    </div>

    <el-table
      v-loading="listLoading"
      :data="list"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
      @selection_change="handleSelectionChange"
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
import { getList } from '@/api/guest'
import waves from '@/directive/waves'
import Pagination from '@/components/Pagination'

export default {
  components :{Pagination},
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
    typeFilter(type){
        if (type)return "学生"
        else return "其他访客"
    },
    tagFilter(type){
        if (type)return "success"
        else return  "danger"
    },
    stuidFilter(student_id){
        console.log(student_id)
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
      fuzzySearch: false,
      mutipleSelection:[],
      total:0,
      limit:0,
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
        this.mutipleSelection =val
    }
  }
}
</script>
