<template>
  <view class="container">
    <view class="imgbox">
      <image class="img-xiaohui" src="@/static/xiaohui.jpg"></image>
    </view>
    <image class="img-indorm" src="@/static/indorm.png"></image>
    <view class="tips">成功进入宿舍！</view>
    <view class="buttonList">
      <button @tap="checkOut">离开宿舍</button>
    </view>
  </view>
</template>

<script>
import navigateTo from '@/api/navigate'
export default {
  data() {
    return {

    }
  },
  methods: {
	checkOut(){
		navigateTo('/pages/guest-form/exit-qrcode')
	}
  }
}
</script>

<style>
.img-indorm {
  position: absolute;
  width: 500rpx;
  height: 400rpx;
  left: 50%;
  transform: translate(-50%, 70%);
}

.tips {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, 200%);
  font-size: 26px;
  width:100%;
  text-align: center;
}

button {
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
  position: relative;
  width: 100%;
  left: 50%;
  transform: translate(-50%, 1000%);
}

</style>
