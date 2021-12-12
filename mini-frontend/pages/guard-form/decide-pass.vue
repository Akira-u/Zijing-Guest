<template>
  <view class="container">
    <view class="imgbox">
      <image class="img-xiaohui" src="@/static/xiaohui.jpg"></image>
    </view>
    <view class="dataTable">
      <uni-section :title="detail_title" type="line"></uni-section>
      <view class="dataList">
      <uni-list>
        <uni-list-item title="访客姓名" :rightText="log.guest.name"></uni-list-item>
        <uni-list-item title="学号" v-if="log.guest.is_student" :rightText="log.guest.student_id"></uni-list-item>
        <uni-list-item title="院系" v-if="log.guest.is_student" :rightText="log.guest.department"></uni-list-item>
        <uni-list-item title="电话" :rightText="log.guest.phone"></uni-list-item>
        <uni-list-item title="来访事由" :rightText="log.purpose"></uni-list-item>
        <uni-list-item title="目的宿舍" :rightText="log.dorm.name"></uni-list-item>
        <uni-list-item title="接待人" :rightText="log.host_student"></uni-list-item>
      </uni-list>
      </view>
    </view>
    <view class="buttonList">
      <button @tap="Pass">通过</button>
      <button @tap="Deny">禁入</button>
    </view>
    <uni-popup ref="credit_popup" type="dialog">
      <uni-popup-dialog mode="base" type="warn" content="请注意：该访客在黑名单中！"></uni-popup-dialog>
    </uni-popup>
  </view>
</template>

<script>
import { registeredGuardRequest } from "@/api/request";
import { decodeOption, reLaunch } from "@/api/navigate";
export default {
  data() {
    return { 
      log: {},
      detail_title:'访客申请（学生）'
    };
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
      if(!res.credit){
        this.$refs.credit_popup.open()
      }
      if(!res.guest.is_student){
        this.detail_title='访客申请（其它访客）'
      }
    });
  },
  methods: {
    Pass() {
      var date = new Date();
      registeredGuardRequest({
        url: "/log/check/",
        method: "POST",
        data: {
          open_id: this.log.guest_id,
          in_time: date,
          approval: "permit",
        },
      }).then((res) => {});
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
.dataTable {
  position: absolute;
  width: 80%;
  left: 50%;
  top: 10%;
  transform: translate(-50%, 10%);
}

.dataList {
  box-shadow: 0 5px 7px 0 rgba(86, 119, 252, 0.2);
}

.buttonList {
  position: absolute;
  width: 100%;
  left: 50%;
  transform: translate(-50%, 250%);
}

button {
  position: relative;
  font-size: 28rpx;
  background: #5677fc;
  color: #fff;
  height: 90rpx;
  line-height: 90rpx;
  border-radius: 50rpx;
  margin: 30px;
  box-shadow: 0 5px 7px 0 rgba(86, 119, 252, 0.2);
}
</style>
