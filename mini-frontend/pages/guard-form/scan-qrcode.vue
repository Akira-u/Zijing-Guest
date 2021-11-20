<template>
  <view class="form-list">
    <image
      @tap="scanQrcode"
      src="/static/scan.jpeg"
	  mode="widthFix"
    ></image>
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
          navigateTo("/pages/guard-form/decide-pass", { code: res.result });
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
</style>
