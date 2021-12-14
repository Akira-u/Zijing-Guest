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
        <uni-list-item title="手机号" :rightText="log.guest.phone"></uni-list-item>
        <uni-list-item title="来访事由" :rightText="log.purpose"></uni-list-item>
        <uni-list-item title="目的宿舍" :rightText="log.dorm.name"></uni-list-item>
        <uni-list-item title="接待人" :rightText="log.host_student"></uni-list-item>
        <uni-list-item title="进入时间" :rightText="getInTime()"></uni-list-item>
      </uni-list>
      </view>
      <view class="buttonList">
        <button @tap="Leave">离开</button>
      </view>
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
      detail_title: '访客信息',
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
      if(!res.guest.is_student){
        that.detail_title='访客申请（其它访客）'
      }
      else{
        that.detail_title='访客申请（学生）'
      }
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
    getInTime() {
      return this.log.in_time.format("yyyy-MM-dd hh:mm:ss");
    }
  },
};
</script>

<style>
.dataTable {
  position: absolute;
  width: 80%;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -55%);
}

.dataList {
  box-shadow: 0 5px 7px 0 rgba(86, 119, 252, 0.2);
}

.buttonList {
  position: relative;
  width: 125%;
  left: 50%;
  transform: translate(-50%, 0%);
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
