<template>
	<view class="container">
		
		<view class="intro">本项目已包含uni ui组件，无需import和注册，可直接使用。在代码区键入字母u，即可通过代码助手列出所有可用组件。光标置于组件名称处按F1，即可查看组件文档。</view>
		<text class="intro">详见：</text>
		<uni-link :href="href" :text="href"></uni-link>
		<button @click="studentVerify">学生访客</button>
		<button>其它访客</button>
		<button>管理员入口</button>

    <el-dialog
      title="提示"
      :visible.sync="dialogVisible"
      width="30%">
      <span>请稍等……</span>
    </el-dialog>

	</view>
</template>

<script>
	export default {
		data() {
			return {
        dailogVisible: false,
				href: 'https://uniapp.dcloud.io/component/README?id=uniui'
			}
		},
		methods: {
			studentVerify(){
        this.dialogVisible = true;
				wx.login({
					success (res1) {
						if (res1.code) {
							wx.request({
                url: 'https://49.232.106.46:8000',
								data: {
									code: res1.code
								},
                success: function(res2){
                  this.dialogVisible = false;
                  console.log(res2);
                  if (res2.data.openid){
                    navigateTo({ url: '/pages/guest-form/guest-form', arg: res2.data });
                  } else {
                    navigateTo({ url: '/pages/guest-form/guest-register'});
                  }
                }
							})
            } else {
							console.log('登陆失败！' + res1.errMsg);
						}
					}
				});
			}
		}
	}
</script>

<style>
	.container {
		padding: 20px;
		font-size: 14px;
		line-height: 24px;
	}
</style>
