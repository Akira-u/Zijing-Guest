<template>
  <view>
    <!-- https://ext.dcloud.net.cn/plugin?id=1287 -->
    <uqrcode ref="guest_qrcode"></uqrcode>
    <!-- TODO:add a 5min countdown -->
    二维码有效期为5分钟，请尽快使用！
    <button @tap="checkResult">审批结束，查看结果</button>
    <mp-dialog :show="dialog_show" @buttontap="checkResult">
      <view class="dialog-submit-content">{{ dialog_text }}</view>
    </mp-dialog>
  </view>
</template>

<script>
import {reLaunch} from '@/api/navigate'
import requestData from '@/api/request'
export default {
  data() {
    return { qrcode_text: '', dialog_show: false, dialog_text: '尚未审批，请稍等...' };
  },
  methods: {
    checkResult() {
      var that = this
      wx.login({
        success: (login_res) => {
          requestData({ url: 'http://49.232.106.46:8000/guest/approve_result', data: { code: login_res.code } })
            .then((approve_res) => {
              if (approve_res.approval === 'permit') {
                that.dialog_text = '审批通过！'
                that.dialog_show = true
                setTimeout(() => {
                  that.dialog_show=false
                }, 1000);
                reLaunch('/pages/guest-form/in-dorm')
              }
              else if (approve_res.approval === 'reject') {
                that.dialog_text = '审批未通过！'
                that.dialog_show = true
                setTimeout(() => {
                  that.dialog_show=false
                }, 1000);
                reLaunch()
              }
              else {
                that.dialog_text = '尚未审批，请稍等...'
                that.dialog_show = true
                setTimeout(() => {
                  that.dialog_show=false
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
          that.qrcode_text = login_res.code+'i'
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


};
</script>

<style>
</style>
