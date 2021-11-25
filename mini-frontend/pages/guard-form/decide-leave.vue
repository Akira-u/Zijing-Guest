<template>
  <view>
    <uni-table border stripe emptyText="暂无更多数据">
      <uni-tr>
        <uni-th>guest</uni-th>
        <uni-td>{{ user.guest }}</uni-td>
      </uni-tr>
      <uni-tr>
        <uni-th>purpose</uni-th>
        <uni-td>{{ user.purpose }}</uni-td>
      </uni-tr>
      <uni-tr>
        <uni-th>target_dorm</uni-th>
        <uni-td>{{ user.target_dorm }}</uni-td>
      </uni-tr>
      <uni-tr>
        <uni-th>host_student</uni-th>
        <uni-td>{{ user.host_student }}</uni-td>
      </uni-tr>
      <uni-tr>
        <uni-th>in_time</uni-th>
        <uni-td>{{ showTime(user.in_time) }}</uni-td>
      </uni-tr>
    </uni-table>
    <button @tap="Leave">离开</button>
  </view>
</template>

<script>
import requestData from "@/api/request";
import { decodeOption, reLaunch } from "@/api/navigate";
export default {
  data() {
    return {
      user: {},
    };
  },
  onLoad(options) {
    decodeOption(options);
    console.log(options.code); //TO DO
    var that = this;
    requestData({
      url: "http://49.232.106.46:8000/log/info/",
      method: "GET",
      data: { code: options.code },
    }).then((res) => {
      console.log({ res: res });
      that.user = res;
    });
  },
  methods: {
    showTime: function (time) {
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
    Leave() {
      var date = new Date();
      console.log(date);
      console.log(this.user.id);
      requestData({
        url: "http://49.232.106.46:8000/log/" + this.user.id + "/",
        method: "PATCH",
        data: {
          out_time: date,
        },
      });
      reLaunch("/pages/guard-form/guard-form");
    },
  },
};
</script>

<style>
</style>
