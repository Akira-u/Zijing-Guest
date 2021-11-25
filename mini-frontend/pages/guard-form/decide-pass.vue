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
        <uni-td>{{ user.in_time }}</uni-td>
      </uni-tr>
      <uni-tr>
        <uni-th>out_time</uni-th>
        <uni-td>{{ user.out_time }}</uni-td>
      </uni-tr>
    </uni-table>
    <button @tap="Pass">通过</button>
    <button @tap="Deny">禁入</button>
  </view>
</template>

<script>
import requestData from "@/api/request";
import { decodeOption } from "@/api/navigate";
export default {
  data() {
    return { user: {} };
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
    Pass() {
      var date = new Date();
      console.log(date);
      console.log(this.user.id);
      requestData({
        url: "http://49.232.106.46:8000/log/" + this.user.id + "/",
        method: "PATCH",
        data: {
          in_time: date,
          approval: "permit",
        },
      });
    },
    Deny() {
      var date = new Date();
      console.log(date);
      console.log(this.user.id);
      requestData({
        url: "http://49.232.106.46:8000/log/" + this.user.id + "/",
        method: "PATCH",
        data: {
          in_time: date,
          approval: "reject",
        },
      });
    },
  },
};
</script>

<style>
</style>
