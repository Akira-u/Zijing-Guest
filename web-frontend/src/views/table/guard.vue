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
          <el-button v-waves class="filter-item" style="margin-left:15px;" type="primary" icon="el-icon-plus" @click="createNewGuard">
            添加
          </el-button>
        </el-col>
      </el-row>
    </div>

    <el-table
      v-loading="listLoading"
      :data="list"
      element-loading-text="加载中"
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
          <el-button v-waves type="primary" icon="el-icon-edit-outline" @click="editGuard(row)">
            编辑
          </el-button>
          <el-button v-waves type="primary" icon="el-icon-delete" @click="deleteGuard(row)">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <pagination v-if="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="limit" @pagination="fetchData" />

    <el-dialog title="分配宿舍楼" :visible.sync="dialogFormVisible" width="40%">
      <el-table
        v-loading="listLoading"
        :data="buildingList"
        element-loading-text="加载中"
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
        <el-button v-waves type="primary" @click="editBuilding">
          保存
        </el-button>
        <el-button v-waves @click="dialogFormVisible = false">
          取消
        </el-button>
      </div>
    </el-dialog>

  </div>
</template>

<script>
import { getList, editBuilding, preCreate, del } from '@/api/guard'
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
    createNewGuard() {
      this.$prompt('请输入新管理员姓名', '添加管理员', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputPattern: /^[\u4E00-\u9FA5]{2,10}[0-9]?$/,
        inputErrorMessage: '仅支持中文姓名（最后可加一位0-9数字）！'
      }).then(({ value }) => {
        let guardName = value
        this.$prompt('请输入admin密码', '验证密码', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          inputPattern: /^[0-9a-zA-z]*/,
          inputErrorMessage: '密码格式错误！'
        }).then(({ value }) => {
          preCreate({ name: guardName, password: value }).then(response => {
            console.log(response)
            if (response.result !== undefined) {
              this.$alert(response.result['name'] + ' 的注册码为：' + response.result['password'], '获取注册码', { confirmButtonText: '点击复制' }).then((res) => {
                this.$copyText(response.result['password']).then((e) => {
                  this.$message({ type: 'success', message: '复制成功，请将注册码发给新管理员，切勿泄露！' })
                }).catch((e) => {
                  this.$alert('复制失败！')
                  console.log(e)
                })
              })
            } else {
              this.$alert('密码错误！')
            }
          })
        })
      }).catch((e) => {
        console.log(e)
      })
    },
    editGuard(row) {
      this.editQuery.open_id = row.open_id
      this.dialogFormVisible = true
    },
    deleteGuard(row) {
      this.$confirm('此操作将删除该管理员, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        del(row.open_id).then(response => {
          this.$message({
            type: 'success',
            message: '删除成功！'
          })
        })
        setTimeout(() => {
          this.fetchData()
        }, 0.5 * 1000)
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    handleCurrentChange(row) {
      this.editQuery.building_id = row.id
    },
    editBuilding() {
      if (this.editQuery.building_id === undefined) {
        this.editQuery.building_id = 1
      }
      editBuilding(this.editQuery)
      setTimeout(() => {
        this.fetchData()
        this.dialogFormVisible = false
      }, 0.5 * 1000)
    }
  }
}
</script>
