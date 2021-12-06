<template>
  <view class="container">
    <view class="imgbox">
      <image class="img-xiaohui" src="@/static/xiaohui.jpg"></image>
    </view>    
    <text>当前楼内有{{ total_guest }}名访客</text>
    <view class="dataTable">
      <uni-table border stripe emptyText="暂无更多数据">
        <uni-tr>
          <uni-th>访客姓名</uni-th>
          <uni-th>进入时间</uni-th>
        </uni-tr>
        <uni-tr
          v-for="(log, index) in logs"
          :key="index"
          v-if="log.out_time == null"
          @tap="checkDetails(log)"
        >
          <uni-td>{{ log.guest_name }}</uni-td>
          <uni-td
            ><uni-dateformat
              :date="log.in_time"
              format="hh:mm:ss"
            ></uni-dateformat
          ></uni-td>
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
    checkDetails: function (log) {
      console.log(log);
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
.dataTable {
  position: absolute;
  width: 80%;
  left: 50%;
  top: 50px;
  transform: translate(-50%, 0%);
}
</style>
