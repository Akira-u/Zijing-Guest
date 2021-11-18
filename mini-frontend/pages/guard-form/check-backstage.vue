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
        <uni-td>{{ user.guest }}</uni-td>
        <uni-td>{{ user.in_time }}</uni-td>
      </uni-tr>
    </uni-table>
  </view>
</template>

<script>
import requestData from "@/api/request";
import navigateTo from "@/api/navigate";
export default {
  data() {
    return { users: [] };
  },
  created() {
    this.update();
  },
  methods: {
    checkDetails: function (user) {
      navigateTo("/pages/guard-form/check-details", {
        code: JSON.stringify(user),
      });
    },
    update() {
      uni.request({
        url: "https://49.232.106.46:8000/guard/log/", 
        method: "GET",
        success: (res) => {
          this.users = res.data.results;
        },
        fail: (res) => {
          console.log("get fail");
        },
      });
      console.log(this.users);
    },
  },
};
</script>

<style>
</style>
