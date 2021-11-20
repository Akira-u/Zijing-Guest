<template>
  <view>
    <!-- https://ext.dcloud.net.cn/plugin?id=1287 -->
    <uqrcode ref="guest_qrcode"></uqrcode>
    <!-- TODO:add a 5min countdown -->
    二维码有效期为5分钟，请尽快使用！
    <button @tap="checkResult">审批结束，查看结果</button>
  </view>
</template>

<script>
import navigateTo from '@/api/navigate'
export default {
  data() {
    return { qrcode_text: '', };
  },
  methods: {
    checkResult(){
      navigateTo('/pages/guest-form/in-dorm')
    }
  },
  onReady() {
    var that = this
    wx.login({
      success: function (login_res) {
        if (login_res.code) {
          that.qrcode_text=login_res.code
          that.$refs.guest_qrcode
            .make({
              size: 354,
              text: that.qrcode_text
            })
            .then((res) => {
              // 返回的res与uni.canvasToTempFilePath返回一致
              console.log(that.qrcode_text);
              // TODO: 轮询后端是否审批通过
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
</style>
