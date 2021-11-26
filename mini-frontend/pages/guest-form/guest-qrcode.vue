<template>
  <view class="QRcodePage">
    <image class="img-xiaohui" src="@/static/xiaohui.jpg"></image>
    <!-- https://ext.dcloud.net.cn/plugin?id=1287 -->
    <uqrcode class= "QRcode" ref="guest_qrcode"></uqrcode>
    <!-- TODO:add a 5min countdown -->
    <view class="tips">二维码有效期为5分钟，请尽快使用！</view>
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
              size: 300,
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
.QRcodePage{
  margin: 10px;
  justify-content: center;
}

.img-xiaohui {
  position: absolute;
  width: 1100rpx;
  height: 1100rpx;
  left: 50%;
  top: 50%;
  transform: translate(-50%,-50%);
  z-index:-1;
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
