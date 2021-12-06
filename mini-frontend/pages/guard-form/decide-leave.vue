<template>
  <view class="container">
    <view class="imgbox">
      <image class="img-xiaohui" src="@/static/xiaohui.jpg"></image>
    </view>
    <view class="dataTable">
      <uni-table border stripe emptyText="暂无更多数据">
        <uni-tr>
          <uni-th>访客姓名</uni-th>
          <uni-td>{{ log.guest_name }}</uni-td>
        </uni-tr>
        <uni-tr>
          <uni-th>来访事由</uni-th>
          <uni-td>{{ log.purpose }}</uni-td>
        </uni-tr>
        <uni-tr>
          <uni-th>目的宿舍</uni-th>
          <uni-td>{{ log.target_dorm }}</uni-td>
        </uni-tr>
        <uni-tr>
          <uni-th>接待人</uni-th>
          <uni-td>{{ log.host_student }}</uni-td>
        </uni-tr>
        <uni-tr>
          <uni-th>进入时间</uni-th>
          <uni-td
            ><uni-dateformat
              :date="log.in_time"
              format="hh:mm:ss"
            ></uni-dateformat
          ></uni-td>
        </uni-tr>
      </uni-table>
    </view>
    <view class="buttonList">
      <button @tap="Leave">离开</button>
    </view>
  </view>
</template>

<script>
import { registeredGuardRequest } from "@/api/request";
import { decodeOption, reLaunch } from "@/api/navigate";
export default {
  data() {
    return {
      log: {},
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
      that.log = res;
    });
  },
  methods: {
    Leave() {
      var date = new Date();
      console.log(date);
      registeredGuardRequest({
        url: "/log/check/",
        method: "POST",
        data: {
          open_id: this.log.guest_id,
          out_time: date,
        },
      });
      reLaunch("/pages/guard-form/guard-form");
    },
  },
};
</script>

<style>
.dataTable {
  position: absolute;
  width: 80%;
  left: 50%;
  top: 20%;
  transform: translate(-50%, 0%);
}

.buttonList {
  position: absolute;
  width: 100%;
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
