<template>
  <view class="container">
    <image class="img-xiaohui" src="@/static/xiaohui.jpg"></image>
    <view class="button_list">
      <button @tap="studentVerify">学生访客</button>
      <button @tap="otherGuestEntry">其它访客</button>
      <button @tap="guardEntry">管理员入口</button>
    </view>
    <mp-dialog :show="DialogShow" @buttontap="onSubmitDialog">
      <view class="dialog-submit-content">请稍候……</view>
    </mp-dialog>
  </view>
</template>

<script>
import navigateTo from "@/api/navigate";
import request from "@/api/request"
export default {
  data() {
    return {
      DialogShow: false,
    };
  },
  onLoad() {
    wx.login({
      success: (login_res) => {
        request({ url: "/guest/status/", data: { code: login_res.code } })
          .then((req_res) => {
            console.log('index onshow ', req_res.status)
            if (req_res.status === 'still in') {
              // if user is in dorm, jump to in-dorm page directly
              uni.redirectTo({ url: '/pages/guest-form/in-dorm' })
            }
          })
      }
    })
  },
  methods: {
    studentVerify() {
      var that = this;
      wx.login({
        success(login_res) {
          that.DialogShow = true;
          request({
            url: "/guest/login/",
            data: { code: login_res.code, }
          })
            .then((req_res) => {
              that.DialogShow = false;
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
            }       
          )
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
          that.DialogShow = true;
          request({
            url: "/guest/login/",
            data: { code: login_res.code, }
          })
            .then((req_res) => {
              that.DialogShow = false;
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
          that.DialogShow = true;
          request({
            url: "/guard/login/",
            data: { code: login_res.code, }
          })
            .then((req_res) => {
              that.DialogShow = false;
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
        },
        fail(login_res) {
          console.log("登录失败！" + login_res.errMsg);
        }
      });
    },
  },
};
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

.container {
  padding: 20px;
  font-size: 14px;
  line-height: 24px;
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
