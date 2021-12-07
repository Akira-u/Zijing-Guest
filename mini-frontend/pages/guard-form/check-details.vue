<template>
  <view class="container">
    <view class="imgbox">
      <image class="img-xiaohui" src="@/static/xiaohui.jpg"></image>
    </view>
    <view class="dataTable">
      <uni-table border stripe emptyText="暂无更多数据">
        <uni-tr>
          <uni-th>访客姓名</uni-th>
          <uni-td>{{ log.guest.name }}</uni-td>
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
      <button @tap="Remind">提醒</button>
    </view>
    <uni-popup class="remindPopup" ref="remindInput" type="dialog">
      <uni-popup ref="popupMessage" type="message">
        <uni-popup-message :type="msgType" :message="errMsg" :duration="1500" />
      </uni-popup>
      <uni-popup-dialog
        class="remindDialog"
        mode="input"
        title="提醒"
        value="同学您好，请尽快签离。"
        placeholder="请输入提醒信息"
        before-close="true"
        @close="dialogClose"
        @confirm="dialogInput"
      />
    </uni-popup>
  </view>
</template>

<script>
import { registeredGuardRequest } from "@/api/request";
import { decodeOption } from "@/api/navigate";
export default {
  data() {
    return {
      log: {},
      remindMsg: "",
      errMsg: "error message",
    };
  },
  onLoad(options) {
    decodeOption(options);
    this.log = JSON.parse(options.code);
    console.log(this.log);
  },
  methods: {
    Remind() {
      console.log("remind");
      this.$refs.remindInput.open();
      //TO DO
    },
    dialogInput(remindMessage) {
      this.remindMsg = remindMessage;

      if (this.remindMsg.length > 25) {
        this.errMsg = "提醒信息长度应不多于25个字符";
        this.$refs.popupMessage.open();
      } else {
        if (this.remindMsg.length == 0) {
          this.remindMsg = "同学您好，请尽快签离。";
        }

        console.log(this.remindMsg);
        this.$refs.remindInput.close();
        console.log(this.log.guest_id);
        registeredGuardRequest({
          url: "/guard/remind/",
          method: "POST",
          data: {
            open_id: this.log.guest_id,
            msg: {
              thing6: {
                value: this.log.guest.name,
              },
              thing1: {
                value: this.log.target_dorm,
              },
              thing5: {
                value: this.remindMsg,
              },
            },
          },
        }).then((res) => {
          console.log({ res: res });
        });
      }
    },
    dialogClose() {
      this.$refs.remindInput.close();
    },
  },
};
</script>

<style>

.dataTable {
  position: absolute;
  width: 80%;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -100%);
}

.buttonList {
  position: absolute;
  width: 100%;
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