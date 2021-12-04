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
    <uni-popup class="remindPopup" ref="remindInput" type="dialog">
      <uni-popup ref="popupMessage" type="message">
			  <uni-popup-message :type="msgType" :message="errMsg" :duration="1500" />
		  </uni-popup>
      <uni-popup-dialog class="remindDialog" mode="input" title="提醒" value="同学您好，您的预计访问时间即将到达，请尽快签离。" placeholder="请输入提醒信息" before-close=true @close="dialogClose" @confirm="dialogInput"/>
    </uni-popup>
  </view>
</template>

<script>
import {registeredGuardRequest} from "@/api/request";
import { decodeOption } from "@/api/navigate";
export default {
  data() {
    return {
      log: {},
      remindMsg: '',
      errMsg: 'error message',
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
      this.$refs["remindInput"].open()
      //TO DO
    },
    dialogInput(remindMessage) {
      this.remindMsg = remindMessage;
			
      if (this.remindMsg.length > 25) {
        this.errMsg = "提醒信息长度应不多于25个字符"
        this.$refs.popupMessage.open();
      }
      else if (this.remindMsg.length == 0) {
        this.errMsg = "提醒信息不能为空"
        this.$refs.popupMessage.open();
      }
      else{
        console.log(this.remindMsg)
        this.$refs["remindInput"].close()
        registeredGuardRequest({
          url: "/guard/remind/",
          method: "POST",
          data: {
		        open_id: this.log.guest_id,
            msg: {
              thing6: {
                value: this.log.guest_name
              },
              thing1: {
                value: this.log.target_dorm
              },
              thing5: {
                value: this.remindMsg
              }
            }
          },
        }).then((res) => {
          console.log({ res: res });
        });
      }
    },
    dialogClose() {
      this.$refs["remindInput"].close()
    }
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

input {
  height: 200px;
}

</style>