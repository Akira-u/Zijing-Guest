<template>
  <div class="app-container">
    <div class="filter-container">
      <el-row>
        <el-col :span="16">
          <el-input v-model="guest_name" placeholder="访客姓名" style="width: 24%;" class="filter-item" @keyup.enter.native="handleFilter" />
          <el-input v-model="listQuery.student_id__icontains" placeholder="学号" style="width: 24%" class="filter-item" @keyup.enter.native="handleFilter" />
          <el-select v-model="listQuery.is_student" placeholder="选择身份" style="width: 12%" class="filter-item" @change="handleFilter">
            <el-option v-for="item in typeOptions" :key="item.key" :label="item.label" :value="item.key" />
          </el-select>
          <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
            查找
          </el-button>
          <el-checkbox v-model="fuzzySearch" class="filter-item" style="margin-left:15px;">
            姓名模糊查找
          </el-checkbox>
        </el-col>
        <el-col :span="8">
          <el-button v-waves class="filter-item" type="primary" icon="el-icon-circle-plus-outline" @click="handleBlackList">
            加入黑名单
          </el-button>
          <el-button v-waves class="filter-item" type="primary" icon="el-icon-circle-plus" @click="handleWhiteList">
            加入白名单
          </el-button>
        </el-col>
      </el-row>
    </div>

    <el-table
      v-loading="listLoading"
      :data="list"
      element-loading-text="Loading"
      stripe
      border
      fit
      highlight-current-row
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" align="center" />
      <el-table-column align="center" label="序号" width="95">
        <template slot-scope="scope">
          {{ scope.$index }}
        </template>
      </el-table-column>
      <el-table-column label="访客姓名">
        <template slot-scope="scope">
          {{ scope.row.name }}
          <el-tag :type="scope.row.is_student | tagFilter">{{ scope.row.is_student | typeFilter }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="信用状态" width="110" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.credit | tagFilter">{{ scope.row.credit | creditFilter }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="学号" width="110" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.student_id | stuidFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column label="手机号" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.phone | phoneFilter }}
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="230" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <el-button type="primary" icon="el-icon-notebook-2" size="mini" @click="checkLog(row)">
            查看近期访问记录
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <pagination v-if="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="limit" @pagination="fetchData" />

    <el-dialog title="查看近期访问记录" :visible.sync="dialogFormVisible" width="65%">
      <el-table
        v-loading="listLoading"
        :data="logList"
        element-loading-text="Loading"
        stripe
        border
        fit
        highlight-current-row
      >
        <el-table-column align="center" label="序号" min-width="5%">
          <template slot-scope="scope">
            {{ scope.$index }}
          </template>
        </el-table-column>
        <el-table-column label="到访宿舍楼" min-width="15%" align="center">
          <template slot-scope="scope">
            {{ scope.row.dormbuilding.name }}
          </template>
        </el-table-column>
        <el-table-column label="到访宿舍" min-width="10%" align="center">
          <template slot-scope="scope">
            {{ scope.row.dorm.name }}
          </template>
        </el-table-column>
        <el-table-column label="来访事由" min-width="20%" align="center">
          <template slot-scope="scope">
            {{ scope.row.purpose }}
          </template>
        </el-table-column>
        <el-table-column label="接待人" min-width="10%" align="center">
          <template slot-scope="scope">
            {{ scope.row.host_student }}
          </template>
        </el-table-column>
        <el-table-column label="进入时间" min-width="20%" align="center">
          <template slot-scope="scope">
            {{ moment(scope.row.in_time).format("YYYY-MM-DD HH:mm:ss") }}
          </template>
        </el-table-column>
        <el-table-column label="离开时间" min-width="20%" align="center">
          <template slot-scope="scope">
            {{ moment(scope.row.out_time).format("YYYY-MM-DD HH:mm:ss") }}
          </template>
        </el-table-column>
      </el-table>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          关闭
        </el-button>
      </div>
    </el-dialog>

  </div>
</template>

<script>
import { getList, getLog, toBlackList, toWhiteList } from '@/api/guest'
import waves from '@/directive/waves'
import Pagination from '@/components/Pagination'

export default {
  components: { Pagination },
  directives: { waves },
  filters: {
    typeFilter(type) {
      if (type) return '学生'
      else return '其他访客'
    },
    tagFilter(type) {
      if (type) return 'success'
      else return 'danger'
    },
    creditFilter(credit) {
      if (credit) return '白名单'
      else return '黑名单'
    },
    stuidFilter(student_id) {
      // console.log(student_id)
      if (student_id === null) return '其他访客无学号'
      else return student_id
    },
    phoneFilter(phone) {
      if (phone === null) return '该访客还未录入手机号'
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
        is_student: undefined
        // ordering: 'id'
      },
      guest_name: undefined,
      fuzzySearch: false,
      multipleSelection: [],
      total: 0,
      limit: 10,
      typeOptions: [{ label: '学生', key: 'true' }, { label: '其他访客', key: 'false' }],
      dialogFormVisible: false,
      logQuery: {
        page: 1,
        guest__open_id: undefined
      },
      logList: null
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
    handleSelectionChange(val) {
      // console.log(val)
      this.multipleSelection = val
    },
    handleBlackList() {
      console.log(this.multipleSelection)
      toBlackList(this.multipleSelection).then(() => {
        this.fetchData()
      })
    },
    handleWhiteList() {
      toWhiteList(this.multipleSelection).then(() => {
        this.fetchData()
      })
    },
    checkLog(row) {
      this.logQuery.guest__open_id = row.guest__open_id
      this.listLoading = true
      getLog(this.logQuery).then(response => {
        this.logList = response.results
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
      this.dialogFormVisible = true
      // this.$nextTick(() => {
      //   this.$refs['dataForm'].clearValidate()
      // })
    }
  }
}
</script>
