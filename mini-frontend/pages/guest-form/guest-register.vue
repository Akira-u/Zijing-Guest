<!-- 蓝色简洁登录页面 -->
<template>
  <view class="t-login">
  <!-- 页面装饰图片 -->
    <image class="img-a" src="@/static/2.png"></image>
    <image class="img-b" src="@/static/3.png"></image>
    <!-- 标题 -->
    <view class="t-b">{{ title }}</view>
    <form class="cl">
      <view class="t-a">
        <image src="@/static/yz.png"></image>
        <input type="text" name="name" placeholder="请输入姓名" maxlength="20" v-model="name" />
      </view>
      <view class="t-a">
        <image src="@/static/sj.png"></image>
        <input type="number" name="phone" placeholder="请输入手机号" maxlength="11" v-model="phone" />
      </view>
      <button @tap="register()">注 册</button>
    </form>
  </view>
</template>
<script>
import {decodeOption} from '@/api/navigate'
import navigateTo from '@/api/navigate'
export default {
  /**
   * 2020年12月1日   李新雷编写（练习）  适用所有app登录
   * vue版本简洁又美观的登录页面（个人感觉插件市场的登录都不太好看，哈哈 O(∩_∩)O）
   * 该模板只是登录模板：验证、倒计时等都已经写好，
   * 如果需要注册（注册可以设计在登录按钮下方），
   * 直接复制该页面稍微改动即可
   */
  data() {
    return {
      title: '注册', //填写logo或者app名称，也可以用：欢迎回来，看您需求
      phone: '', //手机号码
      name: '' //姓名
    };
  },
  onLoad(options) {
    decodeOption(options)
  },
  methods: {
    //当前注册按钮操作
    register() {
      var that = this;
      if (!that.name.length) {
        uni.showToast({ title: '请输入姓名', icon: 'none' });
        return;
      }
      if (!that.phone) {
        uni.showToast({ title: '请输入手机号', icon: 'none' });
        return;
      }
      if (!/^[1][3,4,5,7,8,9][0-9]{9}$/.test(that.phone)) {
        uni.showToast({ title: '请输入正确手机号', icon: 'none' });
        return;
	  }
      wx.login({
        success(res1) {
          if (res1.code) {
            console.log(that.phone);
            wx.request({
              url: 'https://49.232.106.46:8000/guard/user/',
              data: {
                code: res1.code,
                phone: that.phone,
                name: that.name,
			  },
            method: 'POST',
            })
          } else {
            console.log('登陆失败！' + res1.errMsg);
          }
        }
      });
    }
  }
};
</script>
<style>
.img-a {
  position: absolute;
  width: 100%;
  top: -280rpx;
  right: -100rpx;
}
.img-b {
  position: absolute;
  width: 50%;
  bottom: 0;
  left: -50rpx;
  margin-bottom: -200rpx;
}
.t-login {
  width: 600rpx;
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
  font-size: 46rpx;
  color: #000;
  padding: 300rpx 0 120rpx 0;
  font-weight: bold;
}

.t-login {
  position: absolute;
  right: 22rpx;
  top: 22rpx;
  background: #5677fc;
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

.t-login{
  text-align: center;
  width: 250rpx;
  margin: 80rpx auto 0;
}

.t-login {
  float: left;
  width: 50%;
}

.t-login image {
  width: 50rpx;
  height: 50rpx;
}

.t-login {
  text-align: center;
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
  zoom: 1;
}

.cl:after {
  clear: both;
  display: block;
  visibility: hidden;
  height: 0;
  content: '\20';
}
</style>
