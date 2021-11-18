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
    <button @click="Pass">通过</button>
    <button @click="Deny">禁入</button>
  </view>
</template>

<script>
import { decodeOption } from "@/api/navigate";
export default {
  data() {
    return { user: {} };
  },
  onLoad(options) {
    decodeOption(options);
    console.log(options.code);//TO DO
  },
  methods: {
    Pass() {},//TO DO
    Deny() {},
  },
};
</script>

<style>
</style>
