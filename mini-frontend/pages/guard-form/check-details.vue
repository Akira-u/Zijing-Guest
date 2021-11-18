<template>
	<view>
		<uni-table border stripe emptyText="暂无更多数据">
		  <uni-tr>
		    <uni-th>name</uni-th>
		    <uni-td v-text="user.name"></uni-td>
		  </uni-tr>
		  <uni-tr>
		    <uni-th>cumstom_id</uni-th>
		    <uni-td v-text="user.custom_id"></uni-td>
		  </uni-tr>
		</uni-table>
	</view>
</template>

<script>
 data() {
    return {user: {},};
  },
  onLoad(options) {
     decodeOption(options);
     console.log(options.code);
     this.user = JSON.parse(options.code);
     console.log(this.user);
  //    console.log(this.info.name);
  //    console.log(this.info.custom_id);
   },
  methods: {},
};
</script>

<style>
</style>
