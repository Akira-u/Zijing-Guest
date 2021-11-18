<template>
  <view class="container">
    <el-dialog title="提示" width="30%">
      <span>请稍等……</span>
    </el-dialog>

    <view class="intro"
      >本项目已包含uni
      ui组件，无需import和注册，可直接使用。在代码区键入字母u，即可通过代码助手列出所有可用组件。光标置于组件名称处按F1，即可查看组件文档。</view
    >
    <text class="intro">详见：</text>
    <uni-link :href="href" :text="href"></uni-link>
    <button @click="studentVerify">学生访客</button>
    <button>其它访客</button>
    <button @click="guardEntry">管理员入口</button>
  </view>
</template>

<script>
import { decodeOption } from "@/api/navigate";
import navigateTo from "@/api/navigate";
export default {
  data() {
    return {
      //dailogVisible: false,
      href: "https://uniapp.dcloud.io/component/README?id=uniui",
    };
  },
  methods: {
    studentVerify() {
      //this.dialogVisible = true;
      wx.login({
        success(res1) {
          if (res1.code) {
            wx.request({
              url: "https://49.232.106.46:8000/guard/user/",
              data: {
                code: res1.code,
              },
              method: "GET",
              success: function (res2) {
                //this.dialogVisible = false;
                if (res2.data.openid) {
                  navigateTo("/pages/guest-form/guest-form", res2.data);
                } else {
                  navigateTo("/pages/guest-form/guest-register");
                }
              },
            });
          } else {
            console.log("登陆失败！" + res1.errMsg);
          }
        },
      });
    },
    guardEntry() {
      wx.login({
        success(res1) {
          if (res1.code) {
            wx.request({
              url: "https://49.232.106.46:8000/guard/guard/login",
              data: {
                code: res1.code,
              },
              method: "GET",
              success: function (res2) {
                console.log(res2);
                //this.dialogVisible = false;
                if (res2.data.open_id) {
                  navigateTo("/pages/guard-form/guard-form", res2.data);
                } else {
                  navigateTo("/pages/guard-form/guard-register");
                }
              },
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
.container {
  padding: 20px;
  font-size: 14px;
  line-height: 24px;
}
</style>
