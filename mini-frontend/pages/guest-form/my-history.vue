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
      <view class="totalLogs">共查询到{{ total_logs_num }}条访问记录</view>
      <uni-collapse type="line" :accordion="true">
        <uni-collapse-item
          v-for="(log, index) in logs"
          :open="checkNum(index)"
          :key="index"
          :title="askTitle(index)"
        >
          <view class="details">
            <view>来访事由：{{ logs[index].purpose }}</view>
            <view>目的宿舍：{{ logs[index].dorm.name }}</view>
            <view>接待人：{{ logs[index].host_student }}</view>
            <view
              >进入时间：<uni-dateformat
                :date="logs[index].in_time"
                format="yyyy-MM-dd hh:mm:ss"
              ></uni-dateformat
            ></view>
            <view
              >离开时间：<uni-dateformat
                :date="logs[index].out_time"
                format="yyyy-MM-dd hh:mm:ss"
              ></uni-dateformat
            ></view>
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
  </view>
</template>

<script>
import { registeredGuestRequest } from "@/api/request";
import DateFormat from "@/api/date"
export default {
  data() {
    return {
      logs: [],
      current_log: {},
      total_logs_num: 0,
      status: 'more',
      contentText: {
        contentdown: '点击查看更多记录',
        contentrefresh: '加载中',
        contentnomore: '没有更多记录'
      },
      pageNum: 1,
    };
  },
  onReady() {
    registeredGuestRequest({
      url: "/guest/history/",
      data: { page: 1 }
    }).then((res) => {
      console.log('res', res)
      this.logs = res.data
      this.total_logs_num = res.total;
    });
  },
  methods: {
    clickLoadMore() {
      this.status = 'loading';
      registeredGuestRequest({
        url: "/guest/history/",
        data: { page: this.pageNum + 1 },
      }).then((res) => {
        if (res.total > this.pageNum * 10) {
          this.pageNum++;
          this.status = 'more';
          this.logs.push(res.data);
        }
        else if (res.total <= this.pageNum * 10) {
          this.status = 'noMore';
        }
      });
    },
    askTitle: function (index) {
      let approval_text = '错误的访问'
      if (this.logs[index].approval === 'permit') {
        approval_text = '审批通过'
      }
      else if (this.logs[index].approval === 'reject') {
        approval_text = '审批未通过'
      }
      let in_time = new DateFormat()
      return in_time.setTime(new Date(this.logs[index].in_time)).toString('yyyy-0m-0d 0h:0f:0s') + '  ' + approval_text;
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
      registeredGuestRequest({
        url: "/guest/history/",
        data: { page: this.pageNum + 1 },
      }).then((res) => {
        if (res.total > this.pageNum * 10) {
          this.pageNum++;
          this.status = 'more';
          this.logs.push(res.data);
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
</style>