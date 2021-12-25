<script>
import request from "@/api/request";
import navigateTo from "@/api/navigate";
export default {
  onLaunch: function () {
    console.log("App Launch");
  },
  onShow: function (options) {
    if (options.path == "pages/index/index") {
      if (options.referrerInfo.extraData) {
        wx.login({
          success(login_res) {
            request({
              url: "/guest/",
              method: "POST",
              data: {
                code: login_res.code,
                token: options.referrerInfo.extraData.token,
              },
            })
            .then((req_res) => {
              console.log(req_res);
              if (req_res.open_id){
                navigateTo("/pages/guest-form/guest-form", req_res);
              } else{
                navigateTo("/pages/guest-form/guest-register", req_res);
              }
            })
          }
        })
      }
    }
    console.log("App Show");
  },
  onHide: function () {
    console.log("App Hide");
  },
};
</script>

<style>
/*每个页面公共css */
.container {
  height:100%;
  font-size: 14px;
  line-height: 24px;
}

.imgbox {
  position: absolute;
  max-width: 100%;
  max-height: 100%;
  width:100%;
	padding-bottom: 150%;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  overflow: hidden;
}

.img-xiaohui {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: 100%;
  z-index: -1;
  opacity: 0.1;
}
</style>
