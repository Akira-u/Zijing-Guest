<template>
  <view>
    <!-- https://ext.dcloud.net.cn/plugin?id=1287 -->
    <uqrcode ref="guest_qrcode"></uqrcode>
    <!-- TODO:add a 5min countdown -->
    二维码有效期为5分钟，请尽快使用！
  </view>
</template>

<script>
import { decodeOption } from '@/api/navigate'
import navigateTo from '@/api/navigate'
export default {
  data() {
    return { qrcode_text: '', };
  },
  methods: {},
  onLoad(options) {
    decodeOption(options)
    this.qrcode_text = options.code
  },
  onReady() {
    var that = this
    that.$refs.guest_qrcode
      .make({
        size: 354,
        text: that.qrcode_text
      })
      .then((res) => {
        // 返回的res与uni.canvasToTempFilePath返回一致
        console.log(that.qrcode_text);
        var listening_socket = uni.connectSocket({
          url: 'https://c02.whiteffire.cn:8000/guard/guest/',
          success: (connect_res) => {
            console.log('connect success!')
            listening_socket.onMessage((message) => {
              if (message == 'pass') {
                navigateTo("/pages/guest-form/in-dorm")
              }
              else {
                console.log(message)
              }
            })
          },
          fail: (error) => {
            console.log('connect failed')
          }
        })
      });

  }


};
</script>

<style>
</style>
