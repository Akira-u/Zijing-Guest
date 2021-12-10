<template>
  <div class="app-container">
    <div class="filter-container">
      <el-row>
        <el-col :span="24">
          <el-input v-model="guard_name" placeholder="管理员姓名" style="width: 24%;" class="filter-item" @keyup.enter.native="handleFilter" />
          <el-input v-model="listQuery.phone__icontains" placeholder="手机号" style="width: 24%" class="filter-item" @keyup.enter.native="handleFilter" />
          <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
            查找
          </el-button>
          <el-checkbox v-model="fuzzySearch" class="filter-item" style="margin-left:15px;">
            姓名模糊查找
          </el-checkbox>
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
    >
      <el-table-column align="center" label="序号" width="95">
        <template slot-scope="scope">
          {{ scope.$index }}
        </template>
      </el-table-column>
      <el-table-column label="管理员姓名">
        <template slot-scope="scope">
          {{ scope.row.name }}
        </template>
      </el-table-column>
      <el-table-column label="手机号" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.phone | phoneFilter }}
        </template>
      </el-table-column>
      <el-table-column label="管理宿舍楼" width="130" align="center">
        <template slot-scope="scope">
          {{ scope.row.dormbuilding | dormbuildingFilter }}
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="230" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <el-button type="primary" icon="el-icon-edit-outline" @click="editGuard(row)">
            编辑
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <pagination v-if="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="limit" @pagination="fetchData" />

    <el-dialog title="分配宿舍楼" :visible.sync="dialogFormVisible" width="40%">
      <el-table
        v-loading="listLoading"
        :data="buildingList"
        element-loading-text="Loading"
        stripe
        border
        fit
      >
        <el-table-column align="center" label="选择" min-width="30%">
          <template slot-scope="scope">
            <el-radio
              v-model="templateRadio"
              :label="scope.row.id"
              @change.native="handleCurrentChange(scope.row)"
            />
          </template>
        </el-table-column>
        <el-table-column label="宿舍楼" min-width="70%" align="center">
          <template slot-scope="scope">
            {{ scope.row.name }}
          </template>
        </el-table-column>
      </el-table>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="editBuilding">
          保存
        </el-button>
        <el-button @click="dialogFormVisible = false">
          取消
        </el-button>
      </div>
    </el-dialog>

  </div>
</template>

<script>
import { getList, editBuilding } from '@/api/guard'
import { getBuildingList } from '@/api/dorm'
import waves from '@/directive/waves'
import Pagination from '@/components/Pagination'

export default {
  components: { Pagination },
  directives: { waves },
  filters: {
    dormbuildingFilter(dormbuilding) {
      if (dormbuilding === null) return '暂无分配宿舍楼'
      else return dormbuilding.name
    },
    phoneFilter(phone) {
      if (phone === null) return '该管理员还未录入手机号'
      else return phone
    }
  },
  data() {
    return {
      list: null,
      listLoading: true,
      listQuery: {
        page: 1,
        dormbuilding__name: undefined,
        dormbuilding__name__icontains: undefined,
        name: undefined,
        name__icontains: undefined,
        phone: undefined,
        phone__icontains: undefined
        // ordering: 'id'
      },
      guard_name: undefined,
      fuzzySearch: false,
      total: 0,
      limit: 10,
      dialogFormVisible: false,
      buildingList: [],
      buildingTotal: 0,
      editQuery: {
        open_id: undefined,
        building_id: undefined
      },
      templateRadio: false
    }
  },
  created() {
    this.fetchData()
    this.fetchBuilding()
  },
  methods: {
    fetchData() {
      this.listLoading = true
      getList(this.listQuery).then(response => {
        console.log(response)
        this.list = response.results
        this.total = response.count
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    },
    fetchBuilding() {
      this.listLoading = true
      getBuildingList().then(response => {
        this.buildingList = response.results
        this.buildingTotal = response.count
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      if (this.fuzzySearch) {
        this.listQuery.name__icontains = this.guard_name
        this.listQuery.name = undefined
      } else {
        this.listQuery.name__icontains = undefined
        this.listQuery.name = this.guard_name
      }
      this.fetchData()
    },
    editGuard(row) {
      this.editQuery.open_id = row.open_id
      this.dialogFormVisible = true
    },
    handleCurrentChange(row) {
      this.editQuery.building_id = row.id
    },
    editBuilding() {
      if (this.editQuery.building_id === undefined) {
        this.editQuery.building_id = 1
      }
      editBuilding(this.editQuery)
      this.fetchData()
      this.dialogFormVisible = false
    }
  }
}
</script>
