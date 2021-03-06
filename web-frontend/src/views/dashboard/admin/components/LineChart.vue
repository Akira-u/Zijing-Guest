<template>
  <div :class="className" :style="{height:height,width:width}" />
</template>

<script>
import * as echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
import resize from './mixins/resize'

export default {
  mixins: [resize],
  props: {
    className: {
      type: String,
      default: 'chart'
    },
    width: {
      type: String,
      default: '100%'
    },
    height: {
      type: String,
      default: '350px'
    },
    autoResize: {
      type: Boolean,
      default: true
    },
    chartData: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      chart: null
    }
  },
  watch: {
    chartData: {
      deep: true,
      handler(val) {
        console.log(val)
        this.setOptions(val)
      }
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initChart()
    })
  },
  beforeDestroy() {
    if (!this.chart) {
      return
    }
    this.chart.dispose()
    this.chart = null
  },
  methods: {
    initChart() {
      this.chart = echarts.init(this.$el, 'macarons')
      this.setOptions(this.chartData)
    },
    setOptions({ student, other, total } = {}) {
      var today = new Date()
      var date_list = []
      for (var i = 6; i >= 0; i--) {
        var newDate = new Date(today.getTime() - i * 1000 * 60 * 60 * 24)
        var year = newDate.getFullYear()
        var month = (parseInt(newDate.getMonth()) + 1) > 9 ? (parseInt(newDate.getMonth()) + 1) : '0' + (parseInt(newDate.getMonth()) + 1)
        var day = (newDate.getDate()) > 9 ? newDate.getDate() : '0' + newDate.getDate()
        var fullDate = `${year}-${month}-${day}`
        date_list.push(fullDate)
      }
      this.chart.setOption({
        xAxis: {
          data: date_list,
          boundaryGap: false,
          axisTick: {
            show: false
          }
        },
        grid: {
          left: 60,
          right: 60,
          bottom: 20,
          top: 30,
          containLabel: true
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross'
          },
          padding: [5, 10]
        },
        yAxis: {
          axisTick: {
            show: false
          }
        },
        legend: {
          data: ['学生来访', '其他访客', '总计']
        },
        series: [{
          name: '学生来访',
          itemStyle: {
            color: '#FF005A',
            lineStyle: {
              color: '#FF005A',
              width: 2
            }
          },
          smooth: true,
          type: 'line',
          data: student,
          animationDuration: 2800,
          animationEasing: 'cubicInOut'
        },
        {
          name: '其他访客',
          itemStyle: {
            color: '#C0C0C0',
            lineStyle: {
              color: '#C0C0C0',
              width: 2
            }
          },
          smooth: true,
          type: 'line',
          data: other,
          animationDuration: 2800,
          animationEasing: 'cubicInOut'
        },
        {
          name: '总计',
          smooth: true,
          type: 'line',
          itemStyle: {
            color: '#3888fa',
            lineStyle: {
              color: '#3888fa',
              width: 2
            },
            areaStyle: {
              color: '#f3f8ff'
            }
          },
          data: total,
          animationDuration: 2800,
          animationEasing: 'quadraticOut'
        }]
      })
    }
  }
}
</script>
