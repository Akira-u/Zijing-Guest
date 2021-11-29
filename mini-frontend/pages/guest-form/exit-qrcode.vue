<template>
  <view>
    <uqrcode ref="guest_qrcode"></uqrcode>
    请出示二维码给管理员，被扫码后点击结束按钮完成签离。
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
      registeredGuestRequest({ url: 'http://49.232.106.46:8000/guest/status' })
        .then((status_res) => {
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
    wx.login({
      success: function (login_res) {
        if (login_res.code) {
          this.qrcode_text = login_res.code + 'o'
          this.$refs.guest_qrcode
            .make({
              size: 354,
              text: this.qrcode_text
            })
            .then((res) => {
              // 返回的res与uni.canvasToTempFilePath返回一致
              console.log(this.qrcode_text);
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
</style>
