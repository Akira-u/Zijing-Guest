<template>
  <view>
    <uqrcode ref="guestqrcode"></uqrcode>
  </view>
</template>

<script>
export default {
  data() {
    return {};
  },
  methods: {},
  onReady() {
	// https://ext.dcloud.net.cn/plugin?id=1287
    this.$refs.guestqrcode
      .make({
        size: 354,
        text: "uQRCode",
      })
      .then((res) => {
        // 返回的res与uni.canvasToTempFilePath返回一致
        console.log(res);
      });
  },
};
</script>

<style>
</style>
