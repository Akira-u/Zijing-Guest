<template>
  <view class="container">
    <view class="imgbox">
      <image class="img-xiaohui" src="@/static/xiaohui.jpg"></image>
    </view>
    <view class="button_list">
      <button @tap="studentVerify">学生访客</button>
      <button @tap="otherGuestEntry">其它访客</button>
      <button @tap="guardEntry">管理员入口</button>
    </view>
    <uni-popup ref="waiting_popup" type="message" mask-click="false">
      <uni-popup-message
        type="info"
        message="请稍候..."
        :duration="0"
      ></uni-popup-message>
    </uni-popup>
    <uni-popup ref="fail_popup" type="dialog">
      <uni-popup-dialog
        type="error"
        mode="base"
        content="网络错误，请稍后重试！"
      ></uni-popup-dialog>
    </uni-popup>
  </view>
</template>

<script>
import navigateTo from "@/api/navigate";
import request from "@/api/request"
export default {
  data() {
    return {

    };
  },
  onShow() {
    wx.login({
      success: (login_res) => {
        request({ url: "/guest/status/", data: { code: login_res.code } })
          .then((req_res) => {
            console.log(req_res.status)
            if (req_res.status === 'still in') {
              // if user is in dorm, jump to in-dorm page directly
              uni.redirectTo({ url: '/pages/guest-form/in-dorm' })
            }
            else if (req_res.status === 'out') {
              // a student or other guest who has registered and not in dorm now
              // jump to guest-form in case that they may tap wrong entrance
              uni.redirectTo({ url: '/pages/guest-form/guest-form' })
            }
            else if (req_res.status === 'guard') {
              uni.redirectTo({ url: '/pages/guard-form/guard-form' })
            }
            // else: a new user
          })
          .catch((err)=>{
            this.showFailPopup()
          })
      }
    })
  },
  methods: {
    studentVerify() {
      var that = this;
      wx.login({
        success(login_res) {
          that.$refs.waiting_popup.open()
          request({
            url: "/guest/login/",
            data: { code: login_res.code, }
          })
            .then((req_res) => {
              that.$refs.waiting_popup.close()
              console.log(req_res)
              if (req_res.open_id) {
                uni.setStorage({
                  key: 'my_open_id',
                  data: req_res.open_id,
                  fail: (error) => { console.warn(error) }
                })
                navigateTo("/pages/guest-form/guest-form", req_res);
              } else {
                uni.navigateToMiniProgram({
                  "appId": "wx31f880501d44724a",
                  "path": "pages/index/index",
                  "envVersion": "trial",
                  "extraData": {
                    "origin": "miniapp",
                    "type": "id.tsinghua"
                  },
                  success: (res) => {
                    console.log("打开成功", res);
                  },
                  fail: (err) => {
                    console.log(err);
                  },
                })
              }
            })
            .catch((err) => {
              that.showFailPopup()
            })
        },
        fail(login_res) {
          console.log("登录失败！" + login_res.errMsg);
        }
      });
    },
    otherGuestEntry() {
      var that = this;
      wx.login({
        success(login_res) {
          that.$refs.waiting_popup.open()
          request({
            url: "/guest/login/",
            data: { code: login_res.code, }
          })
            .then((req_res) => {
              that.$refs.waiting_popup.close()
              console.log(req_res)
              if (req_res.open_id) {
                uni.setStorage({
                  key: 'my_open_id',
                  data: req_res.open_id,
                  fail: (error) => { console.warn(error) }
                })
                navigateTo("/pages/guest-form/guest-form", req_res);
              } else {
                navigateTo("/pages/guest-form/guest-register");
              }
            })
            .catch((err) => {
              that.showFailPopup()
            })
        },
        fail(login_res) {
          console.log("登录失败！" + login_res.errMsg);
        }
      });
    },
    guardEntry() {
      var that = this
      wx.login({
        success(login_res) {
          that.$refs.waiting_popup.open()
          request({
            url: "/guard/login/",
            data: { code: login_res.code, }
          })
            .then((req_res) => {
              that.$refs.waiting_popup.close()
              console.log(req_res)
              if (req_res.open_id) {
                uni.setStorage({
                  key: 'my_open_id',
                  data: req_res.open_id,
                  success: (result) => { },
                  fail: (error) => { console.warn(error) }
                })
                navigateTo("/pages/guard-form/guard-form", req_res);
              }
              else {
                navigateTo("/pages/guard-form/guard-register");
              }
            })
            .catch((err) => {
              that.showFailPopup()
            })
        },
        fail(login_res) {
          console.log("登录失败！" + login_res.errMsg);
        }
      });
    },
    showFailPopup(){
      this.$refs.waiting_popup.close()
      this.$refs.fail_popup.open()
    }
  },
};
</script>

<style>
.container {
  height:100%;
  font-size: 14px;
  line-height: 24px;
}

.imgbox {
  position: absolute;
  max-width: 100%;
  max-height: 100%;
  width:100%;
	padding-bottom: 150%;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  overflow: hidden;
}

.img-xiaohui {
  position: absolute;
  width: 100%;
  height: 100%;
  z-index: -1;
  opacity: 0.1;
}

.button_list {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
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
</style>
