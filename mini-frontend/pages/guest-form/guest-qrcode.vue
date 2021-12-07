<template>
  <view class="QRcodePage">
    <image class="img-xiaohui" src="@/static/xiaohui.jpg"></image>
    <!-- https://ext.dcloud.net.cn/plugin?id=1287 -->
    <view class="QRcode">
      <uqrcode ref="guest_qrcode"></uqrcode>
      <!-- TODO:add a 5min countdown -->
      <view class="tips">二维码有效期为5分钟，请尽快使用！</view>
    </view>
    <view class="buttonList">
      <button @tap="checkResult">审批结束，查看结果</button>
    </view>
    <uni-popup ref="popupMessage" type="message">
      <uni-popup-message :type="msg_type" :message="msg_text" :duration="1500"/>
    </uni-popup>
  </view>
</template>


<script>
import { reLaunch } from '@/api/navigate'
import { registeredGuestRequest } from '@/api/request'
export default {
  data() {
    return { 
      qrcode_text: '', 
      msg_type: "warn",
      msg_text: '尚未审批，请稍等...' 
    };
  },
  methods: {
    checkResult() {
      registeredGuestRequest({ url: '/guest/approve_result' })
        .then((approve_res) => {
          if (approve_res.approval === 'permit') {
            this.msg_text = '审批通过！'
            this.msg_type = 'success'
            this.$refs.popupMessage.open()
            setTimeout(() => {
              this.$refs.popupMessage.close()
              reLaunch('/pages/guest-form/in-dorm')
            }, 1000);
          }
          else if (approve_res.approval === 'reject') {
            this.msg_text = '审批未通过！'
            this.msg_type = 'error'
            this.$refs.popupMessage.open()
            setTimeout(() => {
              this.$refs.popupMessage.close()
              reLaunch()
            }, 1000);
          }
          else {
            this.msg_text = '尚未审批，请稍等...'
            this.msg_type = 'warn'
            this.$refs.popupMessage.open()
          }
        })
    }
  },
  onReady() {
    var that = this
    wx.login({
      success: function (login_res) {
        if (login_res.code) {
          that.qrcode_text = login_res.code + 'i'
          that.$refs.guest_qrcode
            .make({
              size: 300,
              text: that.qrcode_text
            })
            .then((res) => {
              // 返回的res与uni.canvasToTempFilePath返回一致
              console.log(that.qrcode_text);
            });
        } else {
          console.log(login_res.errMsg)
        }
      }
    })

  }


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

.QRcodePage {
  padding: 20px;
  font-size: 20px;
  line-height: 24px;
  margin: 10px;
  justify-content: center;
}

.QRcode {
  position: absolute;
  left: 50%;
  transform: translate(-50%, 20%);
  justify-content: center;
  z-index: 0;
}

.tips {
  position: relative;
  transform: translate(0%, 150%);
  font-size: 18px;
}

button {
  font-size: 28rpx;
  background: #5677fc;
  color: #fff;
  height: 90rpx;
  line-height: 90rpx;
  border-radius: 50rpx;
  margin: 40px;
  box-shadow: 0 5px 7px 0 rgba(86, 119, 252, 0.2);
}

.buttonList {
  position: relative;
  width: 120%;
  left: 50%;
  transform: translate(-50%, 1000%);
}
</style>

