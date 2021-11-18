<template>
  <view>
	<uni-table border stripe emptyText="暂无更多数据">
		<uni-tr>
			<uni-th>name</uni-th>
			<uni-th>custom_id</uni-th>
		</uni-tr>
		<uni-tr  v-for="user in users" :key="index" @click="checkDetails">
			<uni-td>{{user.name}}</uni-td>
			<uni-td>{{user.custom_id}}</uni-td>
		</uni-tr>
	</uni-table>
  </view>
</template>

<script>
import requestData from "@/api/request";
export default {
  
  data() {
    return {users: [],};
  },
  created() {
	this.update();
    //requestData("http://49.232.106.46:8000/guard/log/", 'get', this.userList)
  },
  methods: {
	update(){
		uni.request({
		  url: "http://49.232.106.46:8000/guard/log/", //仅为示例，并非真实接口地址。
		  method: "GET",
		  success: (res) => {
		    console.log("get success");
		    console.log(res.data.results);
			this.users=res.data.results;
			console.log(this.users);
			console.log(this.users[0].name);
		  },
		  fail: (res) => {
		    console.log("get fail");
		  },
		});
		console.log(this.users);
	},
	checkDetails(){
		navigate()
	}
  },
};
</script>

<style>
</style>
