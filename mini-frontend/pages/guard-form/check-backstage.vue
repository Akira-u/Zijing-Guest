<template>
  <view class="checkBackstage">
    <image class="img-xiaohui" src="@/static/xiaohui.jpg"></image>
    <text>当前楼内有{{ total_guest }}名访客</text>
    <view class="dataTable">
      <uni-table border stripe emptyText="暂无更多数据">
        <uni-tr>
          <uni-th>guest_name</uni-th>
          <uni-th>in_time</uni-th>
        </uni-tr>
        <uni-tr
          v-for="(log, index) in logs"
          :key="index"
          v-if="log.out_time == null"
          @tap="checkDetails(log)"
        >
          <uni-td>{{ log.guest_name }}</uni-td>
          <uni-td>{{ showTime(log.in_time) }}</uni-td>
        </uni-tr>
      </uni-table>
      <uni-pagination
        :show-icon="true"
        :total="total_guest"
        @change="changePage"
      ></uni-pagination>
    </view>
  </view>
</template>

<script>
import { registeredGuardRequest } from "@/api/request";
import navigateTo from "@/api/navigate";
export default {
  data() {
    return {
      logs: {},
      total_guest: 0,
    };
  },
  onLoad() {
    registeredGuardRequest({
      url: "/guard/backstage/",
      data: { page: 1 },
    }).then((res) => {
      console.log(res);
      this.logs = res.data;
      this.total_guest = res.total;
    });
  },
  methods: {
    showTime: function (time) {
      if (time == null) return "null";
      let hh =
        new Date(time).getHours() < 10
          ? "0" + new Date(time).getHours()
          : new Date(time).getHours();
      let mm =
        new Date(time).getMinutes() < 10
          ? "0" + new Date(time).getMinutes()
          : new Date(time).getMinutes();
      return hh + ":" + mm;
    },
    checkDetails: function (log) {
      navigateTo("/pages/guard-form/check-details", {
        code: JSON.stringify(log),
      });
    },
    changePage: function (e) {
      registeredGuardRequest({
        url: "/guard/backstage/",
        data: { page: e.current },
      }).then((res) => {
        console.log(res);
        this.logs = res.data;
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

.checkBackstage {
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
