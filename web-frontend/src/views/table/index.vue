<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input v-if="fuzzySearch==false" v-model="listQuery.guest__name" placeholder="访客姓名" style="width: 150px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-input v-if="fuzzySearch==true" v-model="listQuery.guest__name__icontains" placeholder="访客姓名（模糊）" style="width: 150px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-input v-model="listQuery.guest__student_id" placeholder="学号" style="width: 110px" class="filter-item" @keyup.enter.native="handleFilter" />

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
    >
      <el-table-column align="center" label="ID" width="95">
        <template slot-scope="scope">
          {{ scope.$index }}
        </template>
      </el-table-column>
      <el-table-column label="访客姓名">
        <template slot-scope="scope">
          {{ scope.row.guest.name }}
        </template>
      </el-table-column>
      <el-table-column label="学号" width="110" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.guest.student_id }}</span>
        </template>
      </el-table-column>
      <el-table-column label="手机号" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.guest.phone }}
        </template>
      </el-table-column>
      <el-table-column label="到访宿舍楼" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.target_building }}
        </template>
      </el-table-column>
      <el-table-column label="目的宿舍" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.target_dorm }}
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

    <!-- <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" /> -->

  </div>
</template>

<script>
import { getList } from '@/api/table'
import waves from '@/directive/waves'

export default {
  directives: { waves },
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'gray',
        deleted: 'danger'
      }
      return statusMap[status]
    }
  },
  data() {
    return {
      list: null,
      listLoading: true,
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
      fuzzySearch: false,
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
      this.fetchData()
    },
  }
}
</script>
