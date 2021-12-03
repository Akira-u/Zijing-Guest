<template>
  <view class="checkDetails">
    <image class="img-xiaohui" src="@/static/xiaohui.jpg"></image>
    <view class="dataTable">
      <uni-table border stripe emptyText="暂无更多数据">
        <uni-tr>
          <uni-th>guest_name</uni-th>
          <uni-td>{{ log.guest_name }}</uni-td>
        </uni-tr>
        <uni-tr>
          <uni-th>purpose</uni-th>
          <uni-td>{{ log.purpose }}</uni-td>
        </uni-tr>
        <uni-tr>
          <uni-th>target_dorm</uni-th>
          <uni-td>{{ log.target_dorm }}</uni-td>
        </uni-tr>
        <uni-tr>
          <uni-th>host_student</uni-th>
          <uni-td>{{ log.host_student }}</uni-td>
        </uni-tr>
        <uni-tr>
          <uni-th>in_time</uni-th>
          <uni-td>{{ showTime(log.in_time) }}</uni-td>
        </uni-tr>
      </uni-table>
    </view>
    <view class="buttonList">
      <button @tap="Remind">提醒</button>
    </view>
  </view>
</template>

<script>
import { decodeOption } from "@/api/navigate";
export default {
  data() {
    return {
      log: {},
    };
  },
  onLoad(options) {
    decodeOption(options);
    this.log = JSON.parse(options.code);
  },
  methods: {
    showTime: function (time) {
	  if (time==null) return "null";
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
    Remind() {
      console.log("remind");
      //TO DO
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

.checkDetails {
  padding: 20px;
  font-size: 14px;
  line-height: 24px;
}

.dataTable {
  position: absolute;
  width: 80%;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -100%);
}

.buttonList {
  position: absolute;
  width: 90%;
  left: 50%;
  transform: translate(-50%, 450%);
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