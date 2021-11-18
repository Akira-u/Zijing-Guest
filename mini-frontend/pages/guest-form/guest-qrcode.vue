<template>
  <view>
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
  onReady() {
    var that = this
    var code;// login code should be send to backend as plaintext so that backend can get guest user's openid
    wx.login({
      success: function (login_res) {
        if (login_res.code) {
          code = login_res.code
          that.qrcode_text=code
          that.$refs.guest_qrcode
            .make({
              size: 354,
              text: that.qrcode_text
            })
            .then((res) => {
              // 返回的res与uni.canvasToTempFilePath返回一致
              console.log(that.qrcode_text);
              var listening_socket = uni.connectSocket({
                url: 'https://c02.whiteffire.cn:8000/guard/guest',
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
        } else {
          console.log(login_res.errMsg)
        }
      }
    })
    // https://ext.dcloud.net.cn/plugin?id=1287

  },

};
</script>

<style>
</style>
