<template>
  <view class="checkBackstage">
    <image class="img-xiaohui" src="@/static/xiaohui.jpg"></image>
    <view class="dataTable">
      <uni-table border stripe emptyText="暂无更多数据">
        <uni-tr>
          <uni-th>guest</uni-th>
          <uni-th>in_time</uni-th>
        </uni-tr>
        <uni-tr
          v-for="(user, index) in users"
          :key="index"
          @tap="checkDetails(user)"
        >
          <uni-td>{{ user.guest.name }}</uni-td>
          <uni-td>{{showTime(user.in_time)}}</uni-td>
        </uni-tr>
      </uni-table>
    </view>
  </view>
</template>

<script>
import {registeredGuardRequest} from "@/api/request";
import navigateTo from "@/api/navigate";
export default {
  data() {
    return {
      users: {},
    };
  },
  onLoad() {
    registeredGuardRequest({
      url: "/log/",
    }).then((res) => {
      this.users = res.results;
      console.log(this.users);
    });
  },
  methods: {
	showTime:function(time){
		let hh =
		  new Date(time).getHours() < 10
		    ? "0" + new Date(time).getHours()
		    : new Date(time).getHours();
		let mm =
		  new Date(time).getMinutes() < 10
		    ? "0" + new Date(time).getMinutes()
		    : new Date(time).getMinutes();
		return hh + ":" + mm;
	},
    checkDetails: function (user) {
      navigateTo("/pages/guard-form/check-details", {
        code: JSON.stringify(user),
      });
    },
  },
};
</script>

<style>
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

.checkBackstage {
  padding: 20px;
  font-size: 14px;
  line-height: 24px;
}

.dataTable {
  position: absolute;
  width: 80%;
  left: 50%;
  top: 50px;
  transform: translate(-50%, 0%);
}
</style>
