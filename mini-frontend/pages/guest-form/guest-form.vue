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
      <uni-forms-item required label="到访楼号" name="target_building">
        <view class="targetBuilding">
        <uni-combox 
          :candidates="building_list" 
          v-model="form_data.target_building" 
          placeholder="请选择到访宿舍楼号"
          @input="changeInfo"
        /></view>
      </uni-forms-item>
      <uni-forms-item required label="到访宿舍" name="target_dorm">
        <uni-combox 
          class="targetDorm"
          :candidates="dorm_list" 
          v-model="form_data.target_dorm" 
          placeholder="请选择到访宿舍门牌号"
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
        target_building: '',
        target_dorm: '',
        host_student: '李端',
        purpose: '拿杯'
      },
      msg_text:"您好，欢迎。",
      building_list:[],
      building_info:[],
      dorm_list:[],
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
    request({ url: "/dormbuilding/" })
      .then((res) => {
        that.building_list = []
        that.building_info = res.results
        var len = res.count
        for(var j = 0; j < len; j++) {
          that.building_list.push(res.results[j].name)
        }
      })
  },
  methods: {
    submit() {
      var that=this
      that.$refs.form
        .validate()
        .then((res) => {
          console.log("表单内容：", res);
          registeredGuestRequest({ url: "/log/", method: "POST", data: that.form_data })
            .then((resp_data) => {
              console.log({ resp_data: resp_data })
              wx.requestSubscribeMessage({
                tmplIds: ['7oNPU5JtIAl73LkYMi2PFkPh-Eqf15h8qpRfA4YQVkM'],
                success(res) {
                console.log("subscribe success", res)
                },
                fail(res) {
                  console.log("fail", res)
                },
                complete: function() {
                  navigateTo("/pages/guest-form/guest-qrcode");
                }
              })
            })
        })
        .catch((err) => {
          console.log("表单错误信息：", err);
        });
    },
    viewHistory() {
      navigateTo("/pages/guest-form/my-history")
    },
    changeInfo() {
      var that = this
      var building = that.form_data.target_building
      var index = that.building_list.findIndex(i => i == building)
      if (index > -1){
        index = that.building_info[index].id
        var url = "/dorm/?dormbuilding_id=" + index
        request({ url: url })
          .then((res) => {
            console.log("dorm",res)
            var len = res.count
            that.dorm_list=[]
            for(var j = 0; j < len; j++) {
              that.dorm_list.push(res.results[j].name)
            }
          })
      } 
    }
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
  position:absolute;
}

.uni-forms-item {
  height:120rpx;
}

.uni-combox {
  background: #f8f7fc;
  font-size: 30rpx;
  border-radius: 10rpx;
}

.targetBuilding {
  position: absolute;
  z-index:99;
}

.targetDorm {
  position: absolute;
  z-index:98;
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
