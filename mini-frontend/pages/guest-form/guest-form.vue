<template>
  <view>
    <!-- https://ext.dcloud.net.cn/plugin?id=2773 -->
    <uni-forms ref="form" :modelValue="formData" :rules="rules">
      <uni-forms-item required label="姓名" name="name">
        <uni-easyinput
          type="text"
          v-model="formData.name"
          placeholder="请输入姓名"
        />
      </uni-forms-item>
      <uni-forms-item required label="学号" name="custom_id">
        <uni-easyinput v-model="formData.custom_id" placeholder="请输入学号" />
      </uni-forms-item>
    </uni-forms>
    <button @click="submit">提交</button>
  </view>
</template>

<script>
import CryptoJS from "crypto-js";
import navigateTo from "@/api/navigate";
export default {
  data() {
    return {
      formData: {
        name: undefined,
        cumstom_id: undefined,
      },
      rules: {
        // 对name字段进行必填验证
        name: {
          rules: [
            {
              //   required: true,
              errorMessage: "请输入姓名",
            },
            {
              minLength: 3,
              maxLength: 5,
              errorMessage: "姓名长度在 {minLength} 到 {maxLength} 个字符",
            },
          ],
        },
      },
    };
  },
  methods: {
    submit() {
      this.$refs.form
        .validate()
        .then((res) => {
          console.log("表单内容：", res);

          //   https://developers.weixin.qq.com/miniprogram/dev/framework/open-ability/user-encryptkey.html
          let raw_data = CryptoJS.enc.Utf8.parse(JSON.stringify(res)); //TODO:add time-stamp
          const userCryptoManager = wx.getUserCryptoManager();
          userCryptoManager.getLatestUserKey({
            success({ encryptKey, iv, version, expireTime }) {
              const encryptedData = CryptoJS.AES.encrypt(raw_data, encryptKey, { iv: iv, });
              console.log("key:", encryptKey);
              navigateTo("/pages/guest-form/guest-qrcode", { encrypt_data: encryptedData, });
            },
          });
        })
        .catch((err) => {
          console.log("表单错误信息：", err);
        });
    },
  },
};
</script>

<style>
</style>
