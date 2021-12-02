<template>
  <view class="inDorm">
    <image class="img-a" src="@/static/xiaohui.jpg"></image>
    成功进入宿舍！
    <button @tap="checkOut">离开宿舍</button>
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

.inDorm {
  padding: 20px;
  font-size: 14px;
  line-height: 24px;
}
</style>
