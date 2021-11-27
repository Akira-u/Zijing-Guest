<template>
  <view>
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
</template>

<script>
import registeredRequest from "@/api/request";
import navigateTo from "@/api/navigate";
export default {
  data() {
    return {
      users: {},
    };
  },
  onLoad() {
    registeredRequest({
      url: "http://49.232.106.46:8000/log/",
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
</style>
