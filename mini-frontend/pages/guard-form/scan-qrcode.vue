<template>
  <view class="form-list">
    <image class="img-xiaohui" src="@/static/xiaohui.jpg"></image>
    <image class="scanCode" @tap="scanQrcode" src="/static/scan.jpeg" mode="widthFix"></image>
    <button @tap="scanQrcode">扫码</button>
  </view>
</template>

<script>
import navigateTo from "@/api/navigate";
export default {
  name: "scan",
  data() {
    return {};
  },
  methods: {
    scanQrcode: function () {
      console.log("scan qrcode");
      var that = this;
      wx.scanCode({
        success(res) {
          console.log(res.result);
          var l = res.result.length;
          var code = res.result.substr(0, l - 1);
          if (res.result[l - 1] == "i") {
            navigateTo("/pages/guard-form/decide-pass", { code: code });
          } else if (res.result[l - 1] == "o") {
            navigateTo("/pages/guard-form/decide-leave", { code: code });
          } else {
            console.log("error code");
          }
        },
        fail(res) {
          console.log("fail to scan");
        },
      });
    },
  },
};
</script>

<style>
.form-list {
  padding: 20px;
  font-size: 14px;
  line-height: 24px;
}

.form-list button {
  position: relative;
  font-size: 28rpx;
  background: #5677fc;
  color: #fff;
  height: 90rpx;
  line-height: 90rpx;
  border-radius: 50rpx;
  transform: translate(0%, 900%);
  margin: 40px;
  box-shadow: 0 5px 7px 0 rgba(86, 119, 252, 0.2);
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

.scanCode {
  position: absolute;
  left: 50%;
  top: 30%;
  transform: translate(-50%, -40%);
}
</style>
