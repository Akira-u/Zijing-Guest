<template>
	<view>
		<button @click="scanQrcode">扫码</button>
		<button @click="checkBackstage">查看后台</button>
	</view>
</template>

<script>
export default {
  data() {
    return {};
  },
  methods: {
	scanQrcode() {
	  	uni.navigateTo({ url: '/pages/guard-form/scan-qrcode' })
	  },
    checkBackstage() {
		uni.navigateTo({ url: '/pages/guard-form/check-backstage' })
    },
  },
};
</script>

<style>
</style>
