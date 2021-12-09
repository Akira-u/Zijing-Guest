<template>
  <div>
    <div>
      <el-select v-model="listQuery.dormbuilding_id" placeholder="选择宿舍楼" style="width: 12%" class="filter-item" @change="fetchData">
        <el-option v-for="item in buildinglist" :key="item.id" :label="item.name" :value="item.id" />
      </el-select>
    </div>
    <div v-if="dormtotal>0" class="components-container board">
      <Kanban :key="index" :list="[{name:dorm.student1,id:1},{name:dorm.student2,id:2},{name:dorm.student3,id:3},{name:dorm.student4,id:4}]" class="kanban working" :header-text="dormlist[index].name" v-for="(dorm, index) in dormlist"/> 
    </div>
    
  </div>
</template>
<script>
import { getBuildingList, getDormList } from '@/api/dorm'
import Kanban from '@/components/Kanban'

export default {
  components: {
    Kanban
  },
  data() {
    return {
      dormbuilding: "紫荆一号楼",
      buildinglist: [],
      dormlist: [],
      buildingtotal: 0,
      dormtotal: 0,
      listLoading: false,
      group: 'mission',
      listQuery: {
        dormbuilding_id: 1,
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
      console.log(response)
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
    fetchData(){
      this.listLoading = true
      getDormList(this.listQuery).then(response => {
        this.dormlist = response.results
        this.dormtotal = response.count
        console.log(this.dormlist)
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
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

