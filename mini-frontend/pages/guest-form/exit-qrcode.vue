<template>
  <view>
    请出示二维码给管理员，被扫码后点击结束按钮完成签离。
    <button @tap="exit">结束</button>
  </view>
</template>

<script>
import { reLaunch } from '@/api/navigate'
export default {
  data() {
    return {
      qrcode_text: ''
    }
  },
  methods: {
    exit() {//TODO: 检测扫码状态
      reLaunch()
    }
  },
  onReady() {
    var that = this
    wx.login({
      success: function (login_res) {
        if (login_res.code) {
          that.qrcode_text = login_res.code + '==out'
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
