<template>
  <view>
    <uqrcode ref="guestqrcode"></uqrcode>
  </view>
</template>

<script>
import {decodeOption} from '@/api/navigate'
export default {
  qrcode_text:'',
  data() {
    return {};
  },
  methods: {},
  onLoad(options) {
    decodeOption(options)
    this.qrcode_text=options.encrypt_data
  },
  onReady() {
	// https://ext.dcloud.net.cn/plugin?id=1287
    this.$refs.guestqrcode
      .make({
        size: 354,
        text: this.qrcode_text,
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
