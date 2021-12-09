<template>
  <div class="app-container">
    <div class="filter-container">
      <el-row>
        <el-col :span="20">
          <el-input v-model="guest_name" placeholder="访客姓名" style="width: 25%;" class="filter-item" @keyup.enter.native="handleFilter" />
          <el-input v-model="listQuery.guest__student_id__icontains" placeholder="学号" style="width: 25%" class="filter-item" @keyup.enter.native="handleFilter" />
          <el-select v-model="listQuery.guest__is_student" placeholder="选择身份" style="width: 10%" class="filter-item" @change="handleFilter">
            <el-option v-for="item in statusOptions" :key="item.key" :label="item.label" :value="item.key" />
          </el-select>
          <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
            查找
          </el-button>
          <el-checkbox v-model="fuzzySearch" class="filter-item" style="margin-left:15px;align-self:center;">
            姓名模糊查找
          </el-checkbox>
        </el-col>
        <el-col :span="4">
          <el-button v-waves class="filter-item" type="primary" icon="el-icon-refresh" @click="clearFilter">
            清除当前查找条件
          </el-button>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="12">
          <div class="block">
            <span class="demonstration">进入时间：</span>
            <el-date-picker
              v-model="listQuery.in_time_after"
              type="datetime"
              placeholder="选择日期时间"
              align="right"
            />
            <span class="demonstration"> -- </span>
            <el-date-picker
              v-model="listQuery.in_time_before"
              type="datetime"
              placeholder="选择日期时间"
              align="right"
            />
          </div>
        </el-col>
        <el-col :span="12">
          <div class="block">
            <span class="demonstration">离开时间：</span>
            <el-date-picker
              v-model="listQuery.out_time_after"
              type="datetime"
              placeholder="选择日期时间"
              align="right"
            />
            <span class="demonstration"> -- </span>
            <el-date-picker
              v-model="listQuery.out_time_before"
              type="datetime"
              placeholder="选择日期时间"
              align="right"
            />
          </div>
        </el-col>
      </el-row>
    </div>

    <el-table
      v-loading="listLoading"
      :data="list"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
    >
      <el-table-column align="center" label="ID" width="95">
        <template slot-scope="scope">
          {{ scope.$index }}
        </template>
      </el-table-column>
      <el-table-column label="访客姓名">
        <template slot-scope="scope">
          {{ scope.row.guest.name }}
          <el-tag :type="scope.row.guest.is_student | tagFilter">{{ scope.row.guest.is_student | typeFilter }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="学号" width="110" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.guest.student_id | stuidFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column label="手机号" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.guest.phone | phoneFilter }}
        </template>
      </el-table-column>
      <el-table-column label="信用状态" width="110" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.guest.credit | tagFilter">{{ scope.row.guest.credit | creditFilter }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="到访宿舍楼" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.dormbuilding.name }}
        </template>
      </el-table-column>
      <el-table-column label="到访宿舍" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.dorm.name }}
        </template>
      </el-table-column>
      <el-table-column label="来访事由" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.purpose }}
        </template>
      </el-table-column>
      <el-table-column label="接待人" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.host_student }}
        </template>
      </el-table-column>
      <el-table-column label="进入时间" width="160" align="center">
        <template slot-scope="scope">
          {{ moment(scope.row.in_time).format("YYYY-MM-DD HH:mm:ss") }}
        </template>
      </el-table-column>
      <el-table-column label="离开时间" width="160" align="center">
        <template slot-scope="scope">
          {{ moment(scope.row.out_time).format("YYYY-MM-DD HH:mm:ss") }}
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

    <pagination v-if="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="limit" @pagination="fetchData" />

  </div>
</template>

<script>
import { getList } from '@/api/table'
import waves from '@/directive/waves'
import Pagination from '@/components/Pagination'

export default {
  components: { Pagination },
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
      guest_name: undefined,
      listQuery: {
        page: 1,
        guest__student_id: undefined,
        guest__student_id__icontains: undefined,
        guest__name: undefined,
        guest__name__icontains: undefined,
        guest__is_student: undefined,
        approval: undefined,
        in_time_after: undefined,
        in_time_before: undefined,
        out_time_after: undefined,
        out_time_before: undefined,
        host_student: undefined,
        purpose: undefined,
        target_building: undefined,
        target_dorm: undefined,
        ordering: 'id'
      },
      statusOptions: [{ label: '学生', key: 'true' }, { label: '其他访客', key: 'false' }],
      fuzzySearch: false,
      total: 0,
      limit: 10
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
        this.listQuery.guest__name__icontains = this.guest_name
        this.listQuery.guest__name = undefined
      } else {
        this.listQuery.guest__name__icontains = undefined
        this.listQuery.guest__name = this.guest_name
      }
      this.fetchData()
    },
    clearFilter() {
      this.listQuery = {
        page: 1,
        guest__student_id: undefined,
        guest__student_id__icontains: undefined,
        guest__name: undefined,
        guest__name__icontains: undefined,
        guest__is_student: undefined,
        approval: undefined,
        in_time_after: undefined,
        in_time_before: undefined,
        out_time_after: undefined,
        out_time_before: undefined,
        host_student: undefined,
        purpose: undefined,
        target_building: undefined,
        target_dorm: undefined,
        ordering: 'id'
      }
      this.fetchData()
    }
  }
}
</script>
