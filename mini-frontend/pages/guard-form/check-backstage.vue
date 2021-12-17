<template>
  <view class="container">
    <view class="imgbox">
      <image class="img-xiaohui" src="@/static/xiaohui.jpg"></image>
    </view>
    <scroll-view
      class="dataTable"
      :scroll-top="scrollTop"
      scroll-y="true"
      @scrolltolower="lower"
      scroll-with-animation="true"
    >
      <view class="totalLogs">当前楼内有{{ total_guest }}名访客</view>
      <uni-collapse type="line" :accordion="true">
        <uni-collapse-item
          v-for="(log, index) in logs"
          :open="checkNum(index)"
          :key="index"
          :title="askTitle(index)"
        >
          <view class="details">
            <view>姓名：{{ logs[index].guest.name }}</view>
            <view>手机：{{ logs[index].guest.phone }}</view>
            <template v-if="logs[index].guest.is_student">
              <view>学号：{{ logs[index].guest.student_id }}</view>
              <view>院系：{{ logs[index].guest.department }}</view>
            </template>
            <view>来访事由：{{ logs[index].purpose }}</view>
            <view>目的宿舍：{{ logs[index].dorm.name }}</view>
            <view>接待人：{{ logs[index].host_student }}</view>
            <view
              >进入时间：<uni-dateformat
                :date="logs[index].in_time"
                format="yyyy-MM-dd hh:mm:ss"
              ></uni-dateformat
            ></view>
          </view>
          <view class="buttonList">
            <button @tap="remind(index)">提醒</button>
          </view>
        </uni-collapse-item>
        <view class="example-body">
          <uni-load-more
            :status="status"
            :content-text="contentText"
            @clickLoadMore="clickLoadMore"
          />
        </view>
      </uni-collapse>
    </scroll-view>
    <uni-popup class="remindPopup" ref="remindInput" type="dialog">
      <uni-popup ref="popupMessage" type="message">
        <uni-popup-message
          :type="msgType"
          :message="hintMsg"
          :duration="1500"
        />
      </uni-popup>
      <uni-popup-dialog
        class="remindDialog"
        mode="input"
        title="提醒"
        value="同学您好，请尽快签离。"
        placeholder="请输入提醒信息"
        before-close="true"
        @close="dialogClose(index)"
        @confirm="dialogInput"
      />
    </uni-popup>
  </view>
</template>

<script>
import { registeredGuardRequest } from "@/api/request";
export default {
  data() {
    return {
      logs: [],
      total_guest: 0,
      status: 'more',
      contentText: {
        contentdown: '点击查看更多访客',
        contentrefresh: '加载中',
        contentnomore: '没有更多访客'
      },
      pageNum: 1,
      currentIndex: 0,
      remindMsg: "同学您好，请尽快签离。",
      hintMsg: '提醒信息长度应不多于25个字符',
      msgType: 'error'
    };
  },
  onLoad() {
    registeredGuardRequest({
      url: "/guard/backstage/",
      data: { page: 1 },
    }).then((res) => {
      console.log(res);
      this.logs = res.data;
      this.total_guest = res.total;
    });
  },
  methods: {
    remind(index) {
      this.currentIndex = index;
      this.$refs.remindInput[index].open();
    },
    dialogInput(remindMessage) {
      this.remindMsg = remindMessage;

      if (this.remindMsg.length > 25) {
        this.hintMsg = "提醒信息长度应不多于25个字符";
        this.$refs.popupMessage[this.currentIndex].open();
      } else {
        if (this.remindMsg.length == 0) {
          this.remindMsg = "同学您好，请尽快签离。";
        }
        this.$refs.remindInput[this.currentIndex].close();
        let currentLog = this.logs[this.currentIndex];
        registeredGuardRequest({
          url: "/guard/remind/",
          method: "POST",
          data: {
            open_id: currentLog.guest_id,
            msg: {
              thing6: {
                value: currentLog.guest.name,
              },
              thing1: {
                value: currentLog.dorm.name,
              },
              thing5: {
                value: this.remindMsg,
              },
            },
          },
        }).then((res) => {
          this.hintMsg = "发送成功！";
          this.msgType = 'success'
          this.$refs.popupMessage[this.currentIndex].open();
        });
      }
    },
    dialogClose(index) {
      console.log(index);
      this.$refs.remindInput[index].close();
    },
    clickLoadMore() {
      this.status = 'loading';
      registeredGuardRequest({
        url: "/guard/backstage/",
        data: { page: this.pageNum + 1 },
      }).then((res) => {
        if (res.total > this.pageNum * 10) {
          this.pageNum++;
          this.status = 'more';
          this.logs.push(res.data.filter((value) => {
            // filter invalid logs
            return value.in_time && value.out_time
          }));
        }
        else if (res.total <= this.pageNum * 10) {
          this.status = 'noMore';
        }
      });
    },
    askTitle: function (index) {
      return "访客姓名：" + this.logs[index].guest.name;
    },
    checkNum: function (index) {
      if (index == 0) {
        return true;
      }
      else {
        return false;
      }
    },
    lower() {
      this.status = 'loading';
      registeredGuardRequest({
        url: "/guard/backstage/",
        data: { page: this.pageNum + 1 },
      }).then((res) => {
        if (res.total > this.pageNum * 10) {
          this.pageNum++;
          this.status = 'more';
          this.logs.push(res.data.filter((value) => {
            // filter invalid logs
            return value.in_time && value.out_time
          }));
        }
        else if (res.total <= this.pageNum * 10) {
          this.status = 'noMore';
        }
      });
    },
  },
};
</script>

<style>
.dataTable {
  position: absolute;
  width: 80%;
  height: 80%;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  border-radius: 100rpx;
}

.uni-collapse-item {
  padding: 10px;
  border-radius: 50rpx;
  box-shadow: 0 5px 5px 0 rgba(86, 119, 252, 0.2);
  font-size: 20px;
}
.totalLogs {
  text-align: center;
  font-size: 20px;
}

.details {
  padding: 10px 10px 10px 50px;
}

/* .buttonList {
  position: absolute;
  width: 100%;
  left: 50%;
  transform: translate(-50%, 450%);
} */

button {
  font-size: 28rpx;
  background: #5677fc;
  color: #fff;
  height: 90rpx;
  line-height: 90rpx;
  border-radius: 50rpx;
  margin: 20px;
  box-shadow: 0 5px 7px 0 rgba(86, 119, 252, 0.2);
}

input {
  height: 200px;
}
</style>
