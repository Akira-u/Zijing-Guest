<template>
  <view class="container">
    <image class="img-xiaohui" src="@/static/xiaohui.jpg"></image>
    <view class="button_list">
      <button @tap="studentVerify">学生访客</button>
      <button @tap="otherGuest">其它访客</button>
      <button @tap="guardEntry">管理员入口</button>
    </view>
    <mp-dialog :show="DialogShow" @buttontap="onSubmitDialog">
      <view class="dialog-submit-content">请稍候……</view>
    </mp-dialog>
  </view>
</template>

<script>
import requestData from "@/api/request";
import navigateTo from "@/api/navigate";
export default {
  data() {
    return {
      DialogShow: false,
    };
  },
  methods: {
    studentVerify() {
      var that = this;
      wx.login({
        success(res1) {
          if (res1.code) {
            that.DialogShow = true;
            requestData({
              url: "http://49.232.106.46:8000/guest/login",
              method: "GET",
              data: { code: res1.code },
            }).then((res2) => {
              that.DialogShow = false;
              console.log(res2);
              if (res2.open_id) {
                navigateTo("/pages/guest-form/guest-form", res2);
              } else {
                navigateTo("/pages/guest-form/guest-register");
              }
            });
          } else {
            console.log("登录失败！" + res1.errMsg);
          }
        },
      });
    },
    otherGuest() {
      var that = this;
      wx.login({
        success(res1) {
          if (res1.code) {
            that.DialogShow = true;
            wx.request({
              url: "http://49.232.106.46:8000/guest/login",
              data: {
                code: res1.code,
              },
              method: "GET",
              success: function (res2) {
                that.DialogShow = false;
                console.log(res2.data)
                if (res2.data.open_id) {
                  navigateTo("/pages/guest-form/guest-form", res2.data);
                } else {
                  navigateTo("/pages/guest-form/guest-register");
                }
              },
            });
          } else {
            console.log("登录失败！" + res1.errMsg);
          }
        },
      });
    },
    guardEntry() {
      var that = this
      wx.login({
        success(res1) {
          if (res1.code) {
            requestData({
              url: "http://49.232.106.46:8000/guard/login",
              method: "GET",
              data: { code: res1.code },
            }).then((res2) => {
              console.log(res2);
              if (res2.open_id) {
                navigateTo("/pages/guard-form/guard-form");
              } else {
                navigateTo("/pages/guard-form/guard-register");
              }
            });
          } else {
            console.log("登录失败！" + res1.errMsg);
          }
        },
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
  transform: translate(-50%,-50%);
  z-index:-1;
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
  top:50%;
  transform: translate(-50%,-50%);
  width: 100%;
}

.container button {
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
