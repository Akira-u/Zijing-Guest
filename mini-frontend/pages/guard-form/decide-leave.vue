<template>
  <view class="decideLeave">
    <image class="img-xiaohui" src="@/static/xiaohui.jpg"></image>
    <view class="dataTable">
      <uni-table border stripe emptyText="暂无更多数据">
        <uni-tr>
          <uni-th>guest</uni-th>
          <uni-td>{{ user.guest }}</uni-td>
        </uni-tr>
        <uni-tr>
          <uni-th>purpose</uni-th>
          <uni-td>{{ user.purpose }}</uni-td>
        </uni-tr>
        <uni-tr>
          <uni-th>target_dorm</uni-th>
          <uni-td>{{ user.target_dorm }}</uni-td>
        </uni-tr>
        <uni-tr>
          <uni-th>host_student</uni-th>
          <uni-td>{{ user.host_student }}</uni-td>
        </uni-tr>
        <uni-tr>
          <uni-th>in_time</uni-th>
          <uni-td>{{ showTime(user.in_time) }}</uni-td>
        </uni-tr>
      </uni-table>
    </view>
    <view class="buttonList">
      <button @tap="Leave">离开</button>
    </view>
  </view>
</template>

<script>
import {registeredGuardRequest} from "@/api/request";
import { decodeOption, reLaunch } from "@/api/navigate";
export default {
  data() {
    return {
      user: {},
    };
  },
  onLoad(options) {
    decodeOption(options);
    console.log(options.code); //TO DO
    var that = this;
    registeredGuardRequest({
      url: "/log/info/",
      method: "GET",
      data: { code: options.code },
    }).then((res) => {
      console.log({ res: res });
      that.user = res;
    });
  },
  methods: {
    showTime: function (time) {
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
    Leave() {
      var date = new Date();
      console.log(date);
      console.log(this.user.id);
      registeredGuardRequest({
        url: "/log/" + this.user.id + "/",
        method: "PATCH",
        data: {
          out_time: date,
        },
      });
      reLaunch("/pages/guard-form/guard-form");
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

.decideLeave {
  padding: 20px;
  font-size: 14px;
  line-height: 24px;
}

.dataTable {
  position: absolute;
  width: 80%;
  left: 50%;
  top: 20%;
  transform: translate(-50%, 0%);
}

.buttonList {
  position: absolute;
  width: 90%;
  left: 50%;
  transform: translate(-50%, 480%);
}

button {
  font-size: 28rpx;
  background: #5677fc;
  color: #fff;
  height: 90rpx;
  line-height: 90rpx;
  border-radius: 50rpx;
  margin: 20px;
  box-shadow: 0 5px 7px 0 rgba(86, 119, 252, 0.2);
}
</style>
