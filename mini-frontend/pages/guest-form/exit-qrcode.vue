<template>
  <view class="exitCode">
    <image class="img-xiaohui" src="@/static/xiaohui.jpg"></image>
    <uqrcode ref="guest_qrcode"></uqrcode>
    <view class="tips">请出示二维码给管理员，被扫码后点击结束按钮完成签离。</view>
    <button @tap="exit">结束</button>
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
      registeredGuestRequest({ url: 'http://49.232.106.46:8000/guest/status/' })
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
          that.$refs.guest_qrcode
            .make({
              size: 354,
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
  font-size: 26px;
  line-height: 24px;
  margin: 10px;
  justify-content: center;
}

.uqrcode {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -90%);
}

.tips {
  position: absolute;
  width: 90%;
  left: 50%;
  top: 50%;
  transform: translate(-50%, 150%);
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
  transform: translate(0%, 1000%);
}
</style>
