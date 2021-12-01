<template>
  <view class="guestForm">
    <image class="img-xiaohui" src="@/static/xiaohui.jpg"></image>
    <!-- https://ext.dcloud.net.cn/plugin?id=2773 -->
    <uni-forms class="inputList" ref="form" :modelValue="form_data" :rules="rules">
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
      <uni-forms-item label="访问事由" name="purpose">
        <uni-easyinput
          v-model="form_data.purpose"
          placeholder="请描述访问事由"
        />
      </uni-forms-item>
    </uni-forms>
    <button @tap="submit">提交</button>
  </view>
</template>

<script>
import { registeredGuestRequest } from "@/api/request"
import navigateTo from "@/api/navigate";
export default {
  data() {
    return {
      form_data: {
        target_dorm: '403',
        host_student: '创世洐炎',
        purpose: '拿杯'
      },

      rules: {
        // 对name字段进行必填验证
        name: {
          rules: [
            {
              required: true,
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
  methods: {
    submit() {
      this.$refs.form
        .validate()
        .then((res) => {
          console.log("表单内容：", res);
          registeredGuestRequest({ url: "http://c02.whiteffire.cn:8000/log/", method: "POST", data: this.form_data })
            .then((resp_data) => {
              console.log({ resp_data: resp_data })
              navigateTo("/pages/guest-form/guest-qrcode");
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
.guestForm {
  margin: 10px;
  justify-content: center;
}

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

.inputList {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -120%);
}

.uni-easyinput {
  padding: 0;
  height: 90rpx;
  line-height: 90rpx;
  background: #f8f7fc;
  border: 1px solid #e9e9e9;
  font-size: 28rpx;
  border-radius: 10rpx;
}

.guestForm button {
  font-size: 28rpx;
  background: #5677fc;
  color: #fff;
  height: 90rpx;
  line-height: 90rpx;
  border-radius: 50rpx;
  margin: 40px;
  box-shadow: 0 5px 7px 0 rgba(86, 119, 252, 0.2);
  transform: translate(0%, 800%);
}
</style>
