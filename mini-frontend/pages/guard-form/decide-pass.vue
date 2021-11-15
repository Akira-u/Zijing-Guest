<template>
  <view>
    <h1>INFO</h1>
    <uni-table border stripe emptyText="暂无更多数据">
      <uni-tr>
        <uni-th>name</uni-th>
        <uni-td v-text="info.name"></uni-td>
      </uni-tr>
      <uni-tr>
        <uni-th>cumstom_id</uni-th>
        <uni-td v-text="info.custom_id"></uni-td>
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
    return {
      info: {
        name: undefined,
        custom_id: undefined,
      },
    };
  },
  onLoad(options) {
    decodeOption(options);
    console.log(options.info);
    this.info = JSON.parse(options.info);
    console.log(this.info);
    console.log(this.info.name);
    console.log(this.info.custom_id);
  },
  methods: {
    Pass() {
      uni.request({
        url: "http://49.232.106.46:8000/guard/log/", //仅为示例，并非真实接口地址。
        data: {
          name: "this.info",
          custom_id: 111,
        },
        // header: {
        //     'custom-header': 'hello' //自定义请求头信息
        // },
        method: "POST",
        // success: (res) => {
        //     console.log(res.data);
        // }
      });
    },
    Deny() {},
  },
};
</script>

<style>
</style>
