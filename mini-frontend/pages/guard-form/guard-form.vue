<template>
  <view>
    <button @click="scanQrcode">扫码</button>
    <button @click="checkBackstage">查看后台</button>
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
