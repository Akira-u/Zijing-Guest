<template>
  <view>
    <!-- https://ext.dcloud.net.cn/plugin?id=2773 -->
    <uni-forms ref="form" :modelValue="form_data" :rules="rules">
      <!-- <uni-forms-item required label="姓名" name="name">
        <uni-easyinput v-model="form_data.name" placeholder="请输入姓名" />
      </uni-forms-item> -->
      <uni-forms-item required label="目的宿舍" name="target_dorm">
        <uni-easyinput
          v-model="form_data.target_dorm"
          placeholder="您要拜访的宿舍号"
        />
      </uni-forms-item>
      <uni-forms-item required label="接待人" name="host_student">
        <uni-easyinput
          v-model="form_data.host_student"
          placeholder="您要拜访的人姓名"
        />
      </uni-forms-item>
      <uni-forms-item label="访问事由" name="reason">
        <uni-easyinput v-model="form_data.reason" placeholder="请描述访问事由" />
      </uni-forms-item>
    </uni-forms>
    <button @tap="submit">提交</button>
  </view>
</template>

<script>
import requestData from "@/api/request"
import navigateTo from "@/api/navigate";
export default {
  // components: { uniEasyinput },
  data() {
    return {
      form_data: {
        name: '香香孙沛渝',
        target_dorm: '403',
        host_student: '创世洐炎',
        reason: '拿杯'
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
        target_dorm: {
          rules: [{
            maxLength: 4,
            errorMessage: "宿舍号长度最大为{maxLength}",
          }]
        }
      },
    };
  },
  // onLoad(options) {
  //   decodeOption(options)
  //   this.name = options.name;
  //   this.custom_id = options.custom_id
  // },
  methods: {
    submit() {
      var that=this
      this.$refs.form
        .validate()
        .then((res) => {
          console.log("表单内容：", res);

          //   https://developers.weixin.qq.com/miniprogram/dev/framework/open-ability/user-encryptkey.html
          // let raw_data = CryptoJS.enc.Utf8.parse(JSON.stringify(res));

          // const userCryptoManager = wx.getUserCryptoManager();
          // userCryptoManager.getLatestUserKey({
          //   success({ encryptKey, iv, version, expireTime }) {
          //     encryptKey=CryptoJS.enc.Utf8.parse(encryptKey)
          //     iv=CryptoJS.enc.Utf8.parse(iv)
          //     const encryptedData = CryptoJS.AES.encrypt(JSON.stringify(res), encryptKey, { iv: iv, mode: CryptoJS.mode.CBC,padding: CryptoJS.pad.Pkcs7});
          //     console.log({key: encryptKey.toString(CryptoJS.enc.Utf8) ,data: encryptedData.ciphertext.toString(CryptoJS.enc.Base64),iv:iv.toString(CryptoJS.enc.Utf8)});
          //     navigateTo("/pages/guest-form/guest-qrcode", { ciphertext: encryptedData.ciphertext.toString(CryptoJS.enc.Base64)});
          //   },
          // });
          wx.login({
            success: function(res) {
              if(res.code) {
                that.form_data.code=res.code
                requestData({ url: "https://c02.whiteffire.cn:8000/guard/log/", method: "POST", data: that.form_data })
            .then((res) => {
              console.log({ res_data: res })
              navigateTo("/pages/guest-form/guest-qrcode");
            })
              } else {
                console.log(res.errMsg)
              }
            }
          })
          
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
