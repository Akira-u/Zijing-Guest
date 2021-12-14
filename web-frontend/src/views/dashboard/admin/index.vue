<template>
  <div class="dashboard-editor-container">
    <panel-group :logCount="logCount" :guestCount="guestCount" :dormCount="dormCount" :guardCount="guardCount" @handleSetLineChartData="handleSetLineChartData" />

    <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:32px;">
      <line-chart :chart-data="lineChartData" />
    </el-row>

    <el-row :gutter="32">
      <el-col :xs="24" :sm="24" :lg="8">
        <div class="chart-wrapper">
          <raddar-chart />
        </div>
      </el-col>
      <el-col :xs="24" :sm="24" :lg="8">
        <div class="chart-wrapper">
          <pie-chart :logs_hour="logs_hour" />
        </div>
      </el-col>
      <el-col :xs="24" :sm="24" :lg="8">
        <div class="chart-wrapper">
          <bar-chart :log_weekday="logs_weekday" />
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import PanelGroup from './components/PanelGroup'
import LineChart from './components/LineChart'
import RaddarChart from './components/RaddarChart'
import PieChart from './components/PieChart'
import BarChart from './components/BarChart'

import { getLogStatic, getGuestStatic, getGuardStatic, getDormStatic } from '@/api/remote-search'

export default {
  name: 'DashboardAdmin',
  components: {
    PanelGroup,
    LineChart,
    RaddarChart,
    PieChart,
    BarChart
  },
  data() {
    return {
      logCount: 0,
      logs: {
        student: [0,0,0,0,0,0,0],
        other: [0,0,0,0,0,0,0],
        total: [0,0,0,0,0,0,0]
      },
      logs_weekday: {
        student: [0,0,0,0,0,0,0],
        other: [0,0,0,0,0,0,0],
        total: [0,0,0,0,0,0,0]
      },
      logs_hour: [
        {
          name: '0-5',value:0
        },
        {
          name: '6-11',value:0
        },
        {
          name: '12-17',value:0
        },
        {
          name: '18-23',value:0
        }
      ],
      guestCount: 0,
      guests: undefined,
      guardCount: 0,
      guards: undefined,
      dormCount: 0,
      dorms: undefined,
      lineChartData: {
        student: [0,0,0,0,0,0,0],
        other: [0,0,0,0,0,0,0],
        total: [0,0,0,0,0,0,0]
      },
    }
  },
  created() {
    this.fetchLogData()
    setTimeout(() => {
      this.lineChartData = this.logs
    }, 1.5 * 1000)
  },
  methods: {
    fetchLogData() {
      getLogStatic().then(response => {
        this.logs = response.logs
        this.logCount = response.total_count
        this.logs_weekday = response.logs_weekday
        this.logs_hour = response.logs_hour
      })
      getGuestStatic().then(response => {
        this.guests = response.guests
        this.guestCount = response.total_count
      })
      getGuardStatic().then(response => {
        this.guards = response.guards
        this.guardCount = response.total_count
      })
      getDormStatic().then(response => {
        this.dorms = response.dorms
        this.dormCount = response.total_count
      })
    },
    handleSetLineChartData(type) {
      // this.lineChartData = lineChartData[type]
      this.lineChartData = this.logs
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard-editor-container {
  padding: 32px;
  background-color: rgb(240, 242, 245);
  position: relative;

  .github-corner {
    position: absolute;
    top: 0px;
    border: 0;
    right: 0;
  }

  .chart-wrapper {
    background: #fff;
    padding: 16px 16px 0;
    margin-bottom: 32px;
  }
}

@media (max-width:1024px) {
  .chart-wrapper {
    padding: 8px;
  }
}
</style>
