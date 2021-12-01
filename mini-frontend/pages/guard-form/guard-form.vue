<template>
  <view class= "guardForm">
    <image class="img-xiaohui" src="@/static/xiaohui.jpg"></image>
    <view class="buttonList">
      <button @tap="scanQrcode">扫码</button>
      <button @tap="checkBackstage">查看后台</button>
    </view>
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
.guardForm {
  padding: 20px;
  font-size: 14px;
  line-height: 24px;
}

button {
  position: relative;
  font-size: 28rpx;
  background: #5677fc;
  color: #fff;
  height: 90rpx;
  line-height: 90rpx;
  border-radius: 50rpx;
  margin: 40px;
  box-shadow: 0 5px 7px 0 rgba(86, 119, 252, 0.2);
}

.buttonList {
  position: absolute;
  width: 90%;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}

.img-xiaohui {
  position: absolute;
  width: 1100rpx;
  height: 1100rpx;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  z-index: -1;
  opacity: 0.1;
}
</style>
