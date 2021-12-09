<template>
  <view class="container">
    <view class="imgbox">
      <image class="img-xiaohui" src="@/static/xiaohui.jpg"></image>
    </view>
    <scroll-view class="dataTable" :scroll-top="scrollTop" scroll-y="true" @scrolltolower="lower" scroll-with-animation="true" >
      <view class="totalLogs">当前楼内有{{ total_guest }}名访客</view>
      <uni-collapse type="line" :accordion="true">
        <uni-collapse-item v-for="(log, index) in logs"
        :open="checkNum(index)"
        :key="index"
        :title="askTitle(index)">
          <view class="details">
            <view>姓名：{{ logs[index].guest.name }}</view>
            <view>手机：{{ logs[index].guest.phone }}</view>
            <template v-if="logs[index].guest.is_student">
              <view>学号：{{ logs[index].guest.student_id }}</view>
              <view>院系：{{ logs[index].guest.department }}</view>
            </template>
            <view>来访事由：{{ logs[index].purpose }}</view>
            <view>目的宿舍：{{ logs[index].dorm.id }}</view>
            <view>接待人：{{ logs[index].host_student }}</view>
            <view>进入时间：<uni-dateformat
                :date="logs[index].in_time"
                format="yyyy-MM-dd hh:mm:ss"></uni-dateformat></view>
          </view>
        </uni-collapse-item>
        <view class="example-body">
					<uni-load-more :status="status" :content-text="contentText"  @clickLoadMore="clickLoadMore"/>
				</view>
      </uni-collapse>
    </scroll-view>
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
    clickLoadMore() {
      this.status = 'loading';
      registeredGuardRequest({
        url: "/guard/backstage/",
        data: { page: this.pageNum+1 },
      }).then((res) => {
        if (res.total > this.pageNum * 10){
          this.pageNum++;
          this.status = 'more';
          this.logs.push(res.data.filter((value) => {
          // filter invalid logs
          return value.in_time && value.out_time
        }));
        }
        else if(res.total <= this.pageNum * 10){
          this.status = 'noMore';
        }
      });
    },
    askTitle: function(index) {
      return "访客姓名：" + this.logs[index].guest.name;
    },
    checkNum: function(index) {
      if (index == 0){
        return true;
      }
      else{
        return false;
      }
    },
    lower() {
      this.status = 'loading';
      registeredGuardRequest({
        url: "/guard/backstage/",
        data: { page: this.pageNum+1 },
      }).then((res) => {
        if (res.total > this.pageNum * 10){
          this.pageNum++;
          this.status = 'more';
          this.logs.push(res.data.filter((value) => {
          // filter invalid logs
          return value.in_time && value.out_time
        }));
       }
        else if(res.total <= this.pageNum * 10){
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

.uni-collapse-item{
  padding:10px;
  border-radius: 50rpx;
  box-shadow: 0 5px 5px 0 rgba(86, 119, 252, 0.2);
  font-size:20px;
}
.totalLogs{
  text-align: center;
  font-size: 20px;
}

.details{
  padding:10px 10px 10px 50px;
}
</style>
