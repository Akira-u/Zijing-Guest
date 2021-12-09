<template>
  <view class="container">
    <view class="imgbox">
      <image class="img-xiaohui" src="@/static/xiaohui.jpg"></image>
    </view>
    <!-- https://ext.dcloud.net.cn/plugin?id=2773 -->
    <view>
    <uni-forms
      class="inputList"
      ref="form"
      err-show-type="toast"
      :modelValue="form_data"
      :rules="rules"
    >
      <uni-forms-item required label="电话" name="phone">
        <uni-easyinput
          v-model="form_data.phone"
          placeholder="您的电话号码"
        />
      </uni-forms-item>
      <uni-forms-item required label="目的楼号" name="dorm_id">
        <uni-combox 
          :candidates="candidates" 
          v-model="form_data.dorm_id" 
          placeholder="请选择到访宿舍楼号"
        />
      </uni-forms-item>
      <uni-forms-item required label="目的宿舍" name="target_dorm">
        <!-- TODO: combobox -->
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
          type="textarea" autoHeight
          placeholder="请描述访问事由"
        />
      </uni-forms-item>
    </uni-forms>
    <view class="buttonList">
      <button @tap="submit">提交</button>
      <button @tap="viewHistory">查看申请记录</button>
    </view>
    </view>
    <uni-popup ref="popupMessage" type="message">
      <uni-popup-message type="success" :message="msg_text" :duration="3000"/>
    </uni-popup>
  </view>
</template>

<script>
import { registeredGuestRequest } from "@/api/request"
import request from "@/api/request"
import navigateTo from "@/api/navigate";
export default {
  data() {
    return {
      form_data: {
        phone: "13919198100",
        dorm_id: "1号楼",
        target_dorm: '403A',
        host_student: '李端',
        purpose: '拿杯'
      },
      msg_text:"您好，欢迎。",
      candidates:[
        "1号楼","2号楼","3号楼","4号楼","5号楼","6号楼","7号楼"
      ],
      rules: {
        // 表单验证
        phone: {
          rules: [
            {
              required: true,
              errorMessage: "请输入电话号码",
            },
            {
              minLength: 11,
              maxLength: 11,
              errorMessage: "电话号码长度应为 11 个字符",
            },
          ],
        },
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
  onShow() {
    var that = this;
    wx.login({
      success(login_res) {
        request({
          url: "/guest/login/",
          data: { code: login_res.code, }
        })
          .then((res) => {
            if(res.phone){
              that.form_data.phone = res.phone;
            }
            console.log("res:",res.name)
            that.msg_text = res.name + " 您好，"
            if(res.is_student) {
              that.msg_text += "您以 学生 身份登录。"
            }
            else {
              that.msg_text += "您以 非学生 身份登录。"
            }
            that.$refs.popupMessage.open()
          })
        },
      fail(login_res) {
        console.log("登录失败！" + login_res.errMsg);
      }
    });
    registeredGuestRequest({url:"/guest/status/"})
      .then((res)=>{
        if (res.status === 'still in') {
          // if user is in dorm, jump to in-dorm page directly
          uni.redirectTo({ url: '/pages/guest-form/in-dorm' })
        }
      })
  },
  methods: {
    submit() {
      var that=this
      wx.requestSubscribeMessage({
        tmplIds: ['7oNPU5JtIAl73LkYMi2PFkPh-Eqf15h8qpRfA4YQVkM'],
        success(res) {
          console.log("subscribe success", res)
        },
        fail(res) {
          console.log("fail", res)
        },
        complete: function() {
          that.$refs.form
            .validate()
            .then((res) => {
              console.log("表单内容：", res);
              registeredGuestRequest({ url: "/log/", method: "POST", data: that.form_data })
                .then((resp_data) => {
                  console.log({ resp_data: resp_data })
                  navigateTo("/pages/guest-form/guest-qrcode");
                })
            })
            .catch((err) => {
              console.log("表单错误信息：", err);
            });
        }
      })
    },
    viewHistory() {
      navigateTo("/pages/guest-form/my-history")
    },
  },
};
</script>

<style>
.inputList {
  position: absolute;
  width: 70%;
  height:60%;
  left: 50%;
  top: 10%;
  transform: translate(-50%, 0%);
}

.uni-easyinput {
  line-height: 90rpx;
  background: #f8f7fc;
  font-size: 30rpx;
  border-radius: 10rpx;
}

.uni-forms-item {
  height:120rpx;
}

.uni-combox {
  z-index: 99;
  background: #f8f7fc;
  font-size: 30rpx;
  border-radius: 10rpx;
}

button {
  font-size: 28rpx;
  background: #5677fc;
  color: #fff;
  height: 90rpx;
  line-height: 90rpx;
  border-radius: 50rpx;
  margin: 30px;
  box-shadow: 0 5px 7px 0 rgba(86, 119, 252, 0.2);
}

.buttonList {
  position: absolute;
  width: 100%;
  left: 50%;
  top: 60%;
  transform: translate(-50%, 0%);
}

.uni-popup{
  text-align: center;
}
</style>
