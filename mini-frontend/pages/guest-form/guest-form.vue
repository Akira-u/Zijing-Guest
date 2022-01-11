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
        <uni-forms-item required label="手机号" name="phone">
          <uni-easyinput
            v-model="form_data.phone"
            placeholder="请填写您的手机号码"
          />
        </uni-forms-item>
        <uni-forms-item required label="到访楼号" name="target_building">
          <uni-combox 
            class="targetBuilding"
            :candidates="building_list" 
            v-model="form_data.target_building" 
            placeholder="请选择到访宿舍楼"
            @input="changeInfo"
          />
        </uni-forms-item>
        <uni-forms-item label="到访宿舍" name="target_dorm">
          <uni-combox 
            class="targetDorm"
            :candidates="dorm_list" 
            v-model="form_data.target_dorm" 
            placeholder="请选择到访宿舍门牌号"
          />
        </uni-forms-item>
        <uni-forms-item label="接待人" name="host_student">
          <uni-easyinput
            v-model="form_data.host_student"
            placeholder="请填写您要拜访的人姓名"
          />
        </uni-forms-item>
        <uni-forms-item required label="访问事由" name="purpose">
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
    var that = this;
    return {
      form_data: {
        phone: '',
        target_building: '紫荆3号楼',
        target_dorm: '',
        host_student: '',
        purpose: '打扫卫生'
      },
      msg_text:"您好，欢迎。",
      building_list:[],
      building_info:[],
      dorm_list:[],
      dorm_info:[],
      rules: {
        // 表单验证
        phone: {
          rules: [
            {
              required: true,
              errorMessage: "请输入手机号码",
            },
            {
              minLength: 11,
              maxLength: 11,
              errorMessage: "手机号码长度应为 11 个字符",
            },
          ],
        },
        name: {
          rules: [
            {
              required: false,
              errorMessage: "请输入接待人姓名",
            },
            {
              minLength: 3,
              maxLength: 5,
              errorMessage: "接待人姓名长度在 {minLength} 到 {maxLength} 个字符",
            },
          ],
        },
        target_building: {
          rules: [
            {
              required: true,
              errorMessage: "请选择到访宿舍楼",
            },
            {
              maxLength: 10,
              errorMessage: "宿舍楼号长度最大为{maxLength}",
            },
            {
              validateFunction: function(rule, value, data, callback){
                console.log("validate1",that.building_list)
                var index = that.building_list.findIndex(i => i == value)
                if(index === -1){
                  callback("不存在该宿舍楼")
                }
              }
            },
          ]
        },
        // target_dorm: {
        //   rules: [
        //     {
        //       required: false,
        //       errorMessage: "请选择到访宿舍门牌号",
        //     },
        //     {
        //       maxLength: 4,
        //       errorMessage: "宿舍门牌号长度最大为{maxLength}",
        //     },
        //     {
        //       validateFunction: function(rule, value, data, callback){
        //         console.log("validate2",that.dorm_list)
        //         if(that.dorm_list.length === 0){
        //           callback("请检查到访宿舍楼是否正确")
        //         }
        //         var index = that.dorm_list.findIndex(i => i == value)
        //         if(index === -1){
        //           callback("不存在该宿舍号")
        //         }
        //       }
        //     },
        //   ]
        // },
        purpose:{
          rules: [
            {
              required: true,
              errorMessage: "请输入访问事由",
            },
            {
              maxLength: 100,
              errorMessage: "访问事由长度最大为{maxLength}",
            },
          ]
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
        var len = res.results.length
        for(var j = 0; j < len; j++) {
          that.building_list.push(res.results[j].name)
        }
      })
  },
  onReady() {
    this.$refs.form.setRules(this.rules)
  },
  methods: {
    submit() {
      var that=this
      this.$refs.form
        .validate()
        .then((res) => {
          console.log("表单内容：", res);
          var building = that.form_data.target_building
          var index_building = that.building_list.findIndex(i => i == building)
          var dorm = that.form_data.target_dorm
          var index_dorm = that.dorm_list.findIndex(i => i == dorm)
          registeredGuestRequest({ url: "/log/", method: "POST", data: {
              phone: that.form_data.phone,
              target_building: that.building_info[index_building].id,
              target_dorm: that.dorm_info[index_dorm]?that.dorm_info[index_dorm].id:undefined,
              host_student: that.form_data.host_student,
              purpose: that.form_data.purpose
            }})
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
            that.dorm_info = res.results
            var len = res.results.length
            that.dorm_list = []
            for(var j = 0; j < len; j++) {
              that.dorm_list.push(res.results[j].name)
            }
            that.$refs.form.setRules(that.rules)
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
  width:100%;
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
