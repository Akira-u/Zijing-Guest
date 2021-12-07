<template>
  <div class="app-container">
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
  </div>
</template>

<script>
import { getList } from '@/api/table'

export default {
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
      listLoading: true
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.listLoading = true
      console.log('fetchData')
      getList().then(response => {
        console.log(response)
        this.list = response.results
        this.listLoading = false
      })
    }
  }
}
</script>
