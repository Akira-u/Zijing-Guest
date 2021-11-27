/**
 * 判断请求状态是否成功
 * 参数：http状态码
 * 返回值：[Boolen]
 */
function isHttpSuccess(status) {
    return status >= 200 && status < 300 || status === 304;
}
/**
 * 包装好的request
 * 参数：与wx.request相同。https://developers.weixin.qq.com/miniprogram/dev/api/network/request/wx.request.html
 * 返回值：Promise, 链式调用
 */
function request(options = {}) {
    const {
        success,
        fail,
    } = options;
    if (!options.url) {
        console.warn("request empty url!")
    }
    return new Promise((res, rej) => {
        uni.request(Object.assign(
            options,
            {
                success: (r) => {
                    const isSuccess = isHttpSuccess(r.statusCode);
                    if (isSuccess) {  // 成功的请求状态
                        res(r.data);
                    } else {
                        rej({
                            msg: `网络错误:${r.statusCode}`,
                            detail: r
                        });
                    }
                },
                fail: rej,
            },
        ));
    });
}

/**
 * 在注册后的页面中调用的request，能记住登录状态从而省去wx.login。会检查本地缓存是否有加密的open id，若无则自动再请求一次后存在本地。
 * 参数：与wx.request相同。https://developers.weixin.qq.com/miniprogram/dev/api/network/request/wx.request.html
 * 返回值：Promise, 链式调用
 */
function registeredRequest(options = {}) {
    try {
        options.data.open_id = uni.getStorageSync('open_id')
    } catch (e) {
        // local storage can't get open id due to storage loss
        wx.login({
            success: function (login_res) {
                request({ url: "http://c02.whiteffire.cn:8000/guard/login/", data: { code: login_res.code, } })
                    .then((resp) => {
                        uni.setStorage({
                            key: 'open_id',
                            data: resp.open_id,
                        })
                        options.data.open_id = resp.open_id
                    })

            }
        })

    }
    return request(options)
}
export { request }
export default registeredRequest