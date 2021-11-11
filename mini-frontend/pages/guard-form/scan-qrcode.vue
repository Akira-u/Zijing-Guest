<template>
	<view class='form-list'>
	  <!-- <text>条形码</text> -->
	  <!-- <input :value='scanCodeMsg' type='text' ></input> -->
	  <image class='scan' bindtap='scanQrcode' src='/static/scan.jpeg' mode='widthFix'></image>
	  <button @click="scanQrcode">扫码</button>
	</view>
</template>

<script>
	export default {
		name: "scan",
		data() {
			return {
				scanCodeMsg: "123",
			}
		},
		methods: {
		scanQrcode:function() {
		console.log("scan qrcode")
		  var that = this;
		  wx.scanCode({ //扫描API
		    success(res) { //扫描成功
		      console.log(res.result) //输出回调信息
			  uni.navigateTo({ url: '/pages/guard-form/decide-pass?info=' + res.result})
			  //this.$set(this.data,"scanCodeMsg",res.result)
		      // that.setData({
		      //   scanCodeMsg: res
		      // });
		      // wx.showToast({
		      //   title: '成功',
		      //   duration: 1000
		      // })
		    },
			fail(res) {
				console.log("fail to scan")
			}
		  })
		},
		},
		
			//创建扫描控件
		
	}
</script>

<style>
</style>
