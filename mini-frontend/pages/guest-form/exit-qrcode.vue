<template>
  <view class="exitCode">
    <image class="img-xiaohui" src="@/static/xiaohui.jpg"></image>
    <view class="QRcode">
      <uqrcode ref="exit_qrcode"></uqrcode>
      <view class="tips">请出示二维码给管理员，被扫码后点击结束按钮完成签离。</view>
    </view>
    <view class="buttonList">
      <button @tap="exit">结束</button>
    </view>
    <mp-dialog :show="dialog_show" @buttontap="exit">
      <view class="dialog-submit-content">{{ dialog_text }}</view>
    </mp-dialog>
  </view>
</template>

<script>
import { reLaunch } from '@/api/navigate'
import { registeredGuestRequest } from '@/api/request'
export default {
  data() {
    return {
      qrcode_text: ''
    }
  },
  methods: {
    exit() {
      registeredGuestRequest({ url: '/guest/status/' })
        .then((status_res) => {
          console.log(status_res)
          if (status_res.status === 'out') {
            this.dialog_show = true
            this.dialog_text = '签离成功！'
            setTimeout(() => {
              this.dialog_show = false
            }, 1000);
            reLaunch()
          }
          else {
            this.dialog_show = true
            this.dialog_text = '请让宿舍管理员扫码！'
            setTimeout(() => {
              this.dialog_show = false
            }, 1000);
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

.exitCode {
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
}

.tips {
  position: relative;
  transform: translate(0%, 70%);
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
