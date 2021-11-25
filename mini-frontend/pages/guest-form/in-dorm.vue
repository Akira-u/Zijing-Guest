<template>
  <view>
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
</style>
