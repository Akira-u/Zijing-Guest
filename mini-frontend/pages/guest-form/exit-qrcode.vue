<template>
  <view class="container">
    <view class="imgbox">
      <image class="img-xiaohui" src="@/static/xiaohui.jpg"></image>
    </view>
    <view class="QRcode">
      <uqrcode ref="exit_qrcode"></uqrcode>
      <view class="tips">请出示二维码给管理员，被扫码后点击结束按钮完成签离。</view>
    </view>
    <view class="buttonList">
      <button @tap="exit">结束</button>
    </view>
     <uni-popup ref="exit_popup" type="message">
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
      msg_text: '请让宿舍管理员扫码！'
    }
  },
  methods: {
    exit() {
      registeredGuestRequest({ url: '/guest/status/' })
        .then((status_res) => {
          console.log(status_res)
          if (status_res.status === 'out') {
            this.$refs.exit_popup.open()
            this.msg_text = '签离成功！'
            setTimeout(() => {
              this.dialog_show = false
              reLaunch()
            }, 1000);
          }
          else {
            this.$refs.exit_popup.open()
            this.msg_text = '请让宿舍管理员扫码！'
          }
        })

    }
  },
  onReady() {
    var that = this
    wx.login({
      success: function (login_res) {
        if (login_res.code) {
          that.qrcode_text = login_res.code + 'o'
          that.$refs.exit_qrcode
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
}
</script>

<style>
.QRcode {
  position: absolute;
  left: 50%;
  transform: translate(-50%, 20%);
  justify-content: center;
}

.tips {
  position: absolute;
  padding: 40rpx 0 20rpx 0;
  width:100%;
  left: 50%;
  transform: translate(-50%, 0%);
  text-align:center;
  font-size: 20px;
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
  width: 100%;
  left: 50%;
  transform: translate(-50%, 1000%);
}

</style>
