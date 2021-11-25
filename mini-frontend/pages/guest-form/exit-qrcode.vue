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
import requestData from '@/api/request'
export default {
  data() {
    return {
      qrcode_text: ''
    }
  },
  methods: {
    exit() {
      var that = this
      wx.login({
        success: (login_res) => {
          requestData({ url: 'http://49.232.106.46:8000/guest/status', data: { code: login_res.code } })
            .then((status_res) => {
              if (status_res.status === 'out') {
                that.dialog_show = true
                that.dialog_text = '签离成功！'
                setTimeout(() => {
                  that.dialog_show = false
                }, 1000);
                reLaunch()
              }
              else {
                that.dialog_show = true
                that.dialog_text = '请让宿舍管理员扫码！'
                setTimeout(() => {
                  that.dialog_show = false
                }, 1000);
              }
            })
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
</style>
