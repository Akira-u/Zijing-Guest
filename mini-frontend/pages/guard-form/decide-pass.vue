<template>
  <view class="decidePass">
    <image class="img-xiaohui" src="@/static/xiaohui.jpg"></image>
    <view class="dataTable">
      <uni-table border stripe emptyText="暂无更多数据">
        <uni-tr>
          <uni-th>访客姓名</uni-th>
          <uni-td>{{ log.guest.guest_name }}</uni-td>
        </uni-tr>
        <template v-if="log.guest.is_student">
          <uni-tr>
            <uni-th>学号</uni-th>
            <uni-td>{{ log.guest.student_id }}</uni-td>
          </uni-tr>
          <uni-tr>
            <uni-th>院系</uni-th>
            <uni-td>{{ log.guest.department }}</uni-td>
          </uni-tr>
        </template>
        <uni-tr>
          <uni-th>电话</uni-th>
          <uni-td>{{ log.guest.phone }}</uni-td>
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
      </uni-table>
    </view>
    <view class="buttonList">
      <button @tap="Pass">通过</button>
      <button @tap="Deny">禁入</button>
    </view>
  </view>
</template>

<script>
import { registeredGuardRequest } from "@/api/request";
import { decodeOption, reLaunch } from "@/api/navigate";
export default {
  data() {
    return { log: {} };
  },
  onLoad(options) {
    decodeOption(options);
    registeredGuardRequest({
      url: "/log/info/",
      method: "GET",
      data: { code: options.code },
    }).then((res) => {
      console.log({ res: res });
      this.log = res;
    });
  },
  methods: {
    Pass() {
      var date = new Date();
      console.log(date);
      console.log(this.log.guest_id);
      registeredGuardRequest({
        url: "/log/check/",
        method: "POST",
        data: {
          open_id: this.log.guest_id,
          in_time: date,
          approval: "permit",
        },
      }).then((res) => {
        console.log(res);
      });
      reLaunch("/pages/guard-form/guard-form");
    },
    Deny() {
      var date = new Date();
      console.log(date);
      console.log(this.log.guest_id);
      registeredGuardRequest({
        url: "/log/check/",
        method: "POST",
        data: {
          open_id: this.log.guest_id,
          in_time: date,
          approval: "reject",
        },
      }).then((res) => {
        console.log(res);
      });
      uni.navigateBack();
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

.decidePass {
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
  transform: translate(-50%, 250%);
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
