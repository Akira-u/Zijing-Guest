<template>
  <view class="inDorm">
    <image class="img-xiaohui" src="@/static/xiaohui.jpg"></image>
    <image class="img-indorm" src="@/static/indorm.jpg"></image>
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

.img-indorm {
  position: absolute;
  width: 500rpx;
  height: 500rpx;
  left: 50%;
  transform: translate(-50%, 40%);
}

.inDorm {
  padding: 20px;
  font-size: 14px;
  line-height: 24px;
}

.tips {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, 200%);
  font-size: 26px;
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
  width: 120%;
  left: 50%;
  transform: translate(-50%, 1000%);
}

</style>
