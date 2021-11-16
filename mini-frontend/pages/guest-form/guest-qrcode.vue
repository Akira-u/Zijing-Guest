<template>
  <view>
    <uqrcode ref="guest_qrcode"></uqrcode>
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
    this.qrcode_text = options.encrypt_data+options.code//AES ciphertext ends with '==', which seperates cipher and code
  },
  onReady() {
    // https://ext.dcloud.net.cn/plugin?id=1287
    this.$refs.guest_qrcode
      .make({
        size: 354,
        text: this.qrcode_text
      })
      .then((res) => {
        // 返回的res与uni.canvasToTempFilePath返回一致
        console.log(res);
        var listening_socket=uni.connectSocket({
          url: 'https://c02.whiteffire.cn:8000/',
          success: (connect_res) => {
            console.log('connect success!')
            listening_socket.onMessage((message)=>{
              if(message=='pass'){
                navigateTo("/pages/guest-form/in-dorm")
              }
              else{
                console.log(message)
              }
            })
          },
          fail: (error) => {
            console.log('connect failed')
          }
        })
      });
  },
  
};
</script>

<style>
</style>
