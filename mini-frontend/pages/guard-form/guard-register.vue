<template>
  <view class="t-login">
    <!-- 页面装饰图片 -->
    <image class="img-xiaohui" src="@/static/xiaohui.jpg"></image>
    <!-- 标题 -->
    <view class="t-b">{{ title }}</view>
    <form class="cl">
      <view class="t-a">
        <image src="@/static/yz.png"></image>
        <input
          type="text"
          name="name"
          placeholder="请输入姓名"
          maxlength="20"
          v-model="name"
        />
      </view>
      <view class="t-a">
        <image src="@/static/sj.png"></image>
        <input
          type="number"
          name="phone"
          placeholder="请输入手机号"
          maxlength="11"
          v-model="phone"
        />
      </view>
      <button @tap="register">注 册</button>
    </form>
  </view>
</template>

<script>
import request from "@/api/request";
import navigateTo from "@/api/navigate";
export default {
  data() {
    return {
      title: "注册",
      phone: "",
      name: "",
    };
  },
  methods: {
    //当前注册按钮操作
    register() {
      var that = this;
      if (!that.name.length) {
        uni.showToast({ title: "请输入姓名", icon: "none" });
        return;
      }
      if (!that.phone) {
        uni.showToast({ title: "请输入手机号", icon: "none" });
        return;
      }
      if (!/^[1][3,4,5,7,8,9][0-9]{9}$/.test(that.phone)) {
        uni.showToast({ title: "请输入正确手机号", icon: "none" });
        return;
      }
      wx.login({
        success(res1) {
          if (res1.code) {
            console.log(that.phone);
            request({
              url: "http://49.232.106.46:8000/guard/",
              method: "POST",
              data: {
                code: res1.code,
                phone: that.phone,
                name: that.name,
              },
            }).then((res) => {
              navigateTo("/pages/guard-form/guard-form");
            });
          } else {
            console.log("登陆失败！" + res1.errMsg);
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
  transform: translate(-50%, -50%);
  z-index: -1;
  opacity: 0.1;
}

.t-login {
  width: 100%;
  height: 100%;
  margin: 0 auto;
  font-size: 28rpx;
  color: #000;
}

.t-login button {
  font-size: 28rpx;
  background: #5677fc;
  color: #fff;
  height: 90rpx;
  line-height: 90rpx;
  border-radius: 50rpx;
  box-shadow: 0 5px 7px 0 rgba(86, 119, 252, 0.2);
}

.t-login input {
  padding: 0 20rpx 0 120rpx;
  height: 90rpx;
  line-height: 90rpx;
  margin-bottom: 50rpx;
  background: #f8f7fc;
  border: 1px solid #e9e9e9;
  font-size: 28rpx;
  border-radius: 50rpx;
}

.t-login .t-a {
  position: relative;
}

.t-login .t-a image {
  width: 40rpx;
  height: 40rpx;
  position: absolute;
  left: 40rpx;
  top: 28rpx;
  border-right: 2rpx solid #dedede;
  padding-right: 20rpx;
}

.t-login .t-b {
  text-align: left;
  font-size: 60rpx;
  color: #000;
  padding: 0rpx 0 120rpx 0;
  font-weight: bold;
  margin: 10%;
}

.t-login {
  right: 20%;
  color: #fff;
  font-size: 24rpx;
  border-radius: 50rpx;
  height: 50rpx;
  line-height: 50rpx;
  padding: 0 25rpx;
}

.t-login .t-d {
  text-align: center;
  color: #999;
  margin: 80rpx 0;
}

.t-login {
  text-align: center;
  float: left;
  width: 100%;
  margin: 200rpx 0 0 0;
  color: #666;
}

.t-login text {
  margin-left: 20rpx;
  color: #aaaaaa;
  font-size: 27rpx;
}

.t-login .uni-input-placeholder {
  color: #000;
}

.cl {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 80%;
  zoom: 1;
}

.cl:after {
  clear: both;
  display: block;
  visibility: hidden;
  height: 0;
  content: "\20";
}
</style>
