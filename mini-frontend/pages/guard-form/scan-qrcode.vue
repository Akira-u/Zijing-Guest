<template>
  <view class="form-list">
    <image
      class="scan"
      bindtap="scanQrcode"
      src="/static/scan.jpeg"
      mode="widthFix"
    ></image>
    <button @click="scanQrcode">扫码</button>
  </view>
</template>

<script>
import navigateTo from "@/api/navigate";
export default {
  name: "scan",
  data() {
    return {
      scanCodeMsg: "123",
    };
  },
  methods: {
    scanQrcode: function () {
      console.log("scan qrcode");
      var that = this;
      wx.scanCode({
        success(res) {
          console.log(res.result);
          uni.request({
            url: "http://49.232.106.46:8000/guard/log/",
            data: {
              code: res.result,
            },
            method: "POST",
          });
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
