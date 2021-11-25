<template>
  <view class="form-list">
    <image @tap="scanQrcode" src="/static/scan.jpeg" mode="widthFix"></image>
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
</style>
