<template>
  <view class="QRcodePage">
    <image class="img-xiaohui" src="@/static/xiaohui.jpg"></image>
    <!-- https://ext.dcloud.net.cn/plugin?id=1287 -->
    <uqrcode class="QRcode" ref="guest_qrcode"></uqrcode>
    <!-- TODO:add a 5min countdown -->
    <view class="tips">二维码有效期为5分钟，请尽快使用！</view>
    <button @tap="checkResult">审批结束，查看结果</button>
    <mp-dialog :show="dialog_show" @buttontap="checkResult">
      <view class="dialog-submit-content">{{ dialog_text }}</view>
    </mp-dialog>
  </view>
</template>

<script>
import { reLaunch } from '@/api/navigate'
import registeredRequest from '@/api/request'
export default {
  data() {
    return { qrcode_text: '', dialog_show: false, dialog_text: '尚未审批，请稍等...' };
  },
  methods: {
    checkResult() {
      registeredRequest({ url: 'http://49.232.106.46:8000/guest/approve_result' })
        .then((approve_res) => {
          if (approve_res.approval === 'permit') {
            this.dialog_text = '审批通过！'
            this.dialog_show = true
            setTimeout(() => {
              this.dialog_show = false
            }, 1000);
            reLaunch('/pages/guest-form/in-dorm')
          }
          else if (approve_res.approval === 'reject') {
            this.dialog_text = '审批未通过！'
            this.dialog_show = true
            setTimeout(() => {
              this.dialog_show = false
            }, 1000);
            reLaunch()
          }
          else {
            this.dialog_text = '尚未审批，请稍等...'
            this.dialog_show = true
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
.QRcodePage {
  margin: 10px;
  justify-content: center;
}

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

.QRcodePage button {
  font-size: 28rpx;
  background: #5677fc;
  color: #fff;
  height: 90rpx;
  line-height: 90rpx;
  border-radius: 50rpx;
  margin: 40px;
  box-shadow: 0 5px 7px 0 rgba(86, 119, 252, 0.2);
}
</style>
