<template>
  <view class="history">
    <image class="img-xiaohui" src="@/static/xiaohui.jpg"></image>
    <view class="dataTable">
      <uni-table border stripe emptyText="暂无更多数据">
        <uni-tr>
          <uni-th>开始时间</uni-th>
          <uni-th>目的宿舍</uni-th>
        </uni-tr>
        <uni-tr
          v-for="(log, index) in logs"
          :key="index"
          @tap="checkDetails(log)"
        >
          <uni-td
            ><uni-dateformat :date="log.out_time"></uni-dateformat
          ></uni-td>
          <uni-td>{{ log.target_dorm }}</uni-td>
        </uni-tr>
      </uni-table>
      <uni-pagination
        :show-icon="true"
        :total="total_logs_num"
        @change="changePage"
      ></uni-pagination>
    </view>
    <uni-popup ref="detail" type="center">
      <view>
        <uni-table border stripe emptyText="暂无更多数据">
          <uni-tr>
            <uni-th>来访事由</uni-th>
            <uni-td>{{ current_log.purpose }}</uni-td>
          </uni-tr>
          <uni-tr>
            <uni-th>目的宿舍</uni-th>
            <uni-td>{{ current_log.target_dorm }}</uni-td>
          </uni-tr>
          <uni-tr>
            <uni-th>接待人</uni-th>
            <uni-td>{{ current_log.host_student }}</uni-td>
          </uni-tr>
          <uni-tr>
            <uni-th>审批结果</uni-th>
            <uni-td>{{ current_log.approve_result }}</uni-td>
          </uni-tr>
          <template v-if="current_log.approve_result === 'permit'">
            <uni-tr>
              <uni-th>进入时间</uni-th>
              <uni-td
                ><uni-dateformat :date="current_log.in_time"></uni-dateformat
              ></uni-td>
            </uni-tr>
            <uni-tr>
              <uni-th>离开时间</uni-th>
              <uni-td
                ><uni-dateformat :date="current_log.out_time"></uni-dateformat
              ></uni-td>
            </uni-tr>
          </template>
        </uni-table>
      </view>
    </uni-popup>
  </view>
</template>

<script>
import { registeredGuestRequest } from "@/api/request";
export default {
  data() {
    return {
      logs: {},
      current_log: {},
      total_logs_num: 0,
    };
  },
  onLoad() {
    registeredGuestRequest({
      url: "/guest/history/",
      data: { page: 1 }
    }).then((res) => {
      this.logs = res.data
      this.total_logs_num = res.total;
    });
  },
  methods: {
    checkDetails: function (log) {
      this.current_log = log
      this.$refs.detail.open()
    },
    changePage: function (e) {
      registeredGuestRequest({
        url: "/guest/history/",
        data: { page: e.current },
      }).then((res) => {
        this.logs = res.data
      });
    },
  },

};
</script>

<style>
.img-xiaohui {
  position: absolute;
  width: 1100rpx;
  height: 1100rpx;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  z-index: -1;
  opacity: 0.1;
}

.history {
  padding: 20px;
  font-size: 14px;
  line-height: 24px;
}

.dataTable {
  position: absolute;
  width: 80%;
  left: 50%;
  top: 50px;
  transform: translate(-50%, 0%);
}
</style>