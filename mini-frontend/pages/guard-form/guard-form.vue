<template>
  <view>
    <button @tap="scanQrcode">扫码</button>
    <button @tap="checkBackstage">查看后台</button>
  </view>
</template>

<script>
import navigateTo from "@/api/navigate";
export default {
  data() {
    return {};
  },
  methods: {
    scanQrcode() {
      navigateTo("/pages/guard-form/scan-qrcode");
    },
    checkBackstage() {
      navigateTo("/pages/guard-form/check-backstage");
    },
  },
};
</script>

<style>
</style>
