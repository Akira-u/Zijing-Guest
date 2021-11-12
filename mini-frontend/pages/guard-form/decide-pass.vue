<template>
  <view>
    <h1>INFO</h1>
    <!-- <input :value='info' type='text' ></input> -->
    <text>{{ info }}</text>
    <button @click="Pass">通过</button>
    <button @click="Deny">禁入</button>
  </view>
</template>

<script>
import { decodeOption } from "@/api/navigate";
export default {
  data() {
    return {
      info: {},
    };
  },
  onLoad(options) {
    //option为object类型，会序列化上个页面传递的参数
    decodeOption(options);
    console.log(options.info);
    this.info = options.info;
    //this.$set(this.data, "info", option.info)
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
