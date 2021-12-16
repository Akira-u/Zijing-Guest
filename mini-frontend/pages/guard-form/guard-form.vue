<template>
  <view class="container">
    <view class="imgbox">
      <image class="img-xiaohui" src="@/static/xiaohui.jpg"></image>
    </view>
    <image
      class="scanCode"
      @tap="scanQrcode"
      src="/static/scan.png"
      mode="widthFix"
    ></image>
    <view class="buttonList">
      <button @tap="checkBackstage">查看后台</button>
    </view>
    <uni-popup ref="fail_popup" type="dialog">
      <uni-popup-dialog
        type="error"
        mode="base"
        content="无效二维码！"
      ></uni-popup-dialog>
    </uni-popup>
  </view>
</template>

<script>
import navigateTo from "@/api/navigate";
export default {
  data() {
    return {};
  },
  methods: {
    scanQrcode: function () {
      console.log("scan qrcode");
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
            this.$refs.fail_popup.open()
          }
        },
        fail(res) {
          console.log("fail to scan");
        },
      });
    },
    checkBackstage() {
      navigateTo("/pages/guard-form/check-backstage");
    },
  },
};
</script>

<style>
button {
  position: relative;
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
  position: absolute;
  width: 100%;
  left: 50%;
  top: 70%;
  transform: translate(-50%, -50%);
}

.scanCode {
  position: absolute;
  width: 500rpx;
  height: 500rpx;
  left: 50%;
  top: 30%;
  transform: translate(-50%, -40%);
}
</style>
