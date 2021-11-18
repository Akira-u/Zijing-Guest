<template>
  <view class="form-list">
    <!-- <text>条形码</text> -->
    <!-- <input :value='scanCodeMsg' type='text' ></input> -->
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
import CryptoJS from "crypto-js";
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
        //扫描API
        success(res) {
          //扫描成功
          console.log(res.result); //输出回调信息
		  uni.request({
		  	url: "http://49.232.106.46:8000/guard/log/", //仅为示例，并非真实接口地址。
		  	data: {
		  	  code:res.result,
		  	},
		  	method: "POST",
		  })
		    navigateTo("/pages/guard-form/decide-pass", { code: res.result, });
		  //let raw_data = CryptoJS.enc.Utf8.parse(res.result); //TODO:add time-stamp
		  //console.log(raw_data);
		  // const userCryptoManager = wx.getUserCryptoManager();
		  // userCryptoManager.getLatestUserKey({
		  //   success({ encryptKey, iv, version, expireTime }) {
		  //     const decryptedData = CryptoJS.AES.decrypt(res.result, encryptKey, { iv: iv, });
		  //     console.log({key: encryptKey,data: decryptedData.toString(CryptoJS.enc.Utf8)});
		  //     navigateTo("/pages/guard-form/decide-pass", { info: decryptedData.toString(CryptoJS.enc.Utf8), });
		  //   },
		  // });
          //navigateTo("/pages/guard-form/decide-pass", { info: res.result });
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
          console.log("fail to scan");
        },
      });
    },
  },

  //创建扫描控件
};
</script>

<style>
</style>
