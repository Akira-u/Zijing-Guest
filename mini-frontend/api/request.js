var base_url = "http://c02.whiteffire.cn:8000"
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
    if (options.url[0] !== '/') {
        console.log(options.url, ' without \'/\' at the beginning')
    }
    options.url = base_url + options.url
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
function registeredGuardRequest(options = {}) {
    if (options.data === undefined) {
        options.data = {}
    }
    try {
        options.data.my_open_id = uni.getStorageSync('my_open_id')
    } catch (e) {
        // local storage can't get open id due to storage loss
        wx.login({
            success: function (login_res) {
                request({ url: "/guard/login/", data: { code: login_res.code, } })
                    .then((resp) => {
                        uni.setStorage({
                            key: 'my_open_id',
                            data: resp.open_id,
                        })
                        options.data.my_open_id = resp.open_id
                    })

            }
        })

    }
    return request(options)
}
function registeredGuestRequest(options = {}) {
    if (options.data === undefined) {
        options.data = {}
    }
    try {
        options.data.my_open_id = uni.getStorageSync('my_open_id')
    } catch (e) {
        // local storage can't get open id due to storage loss
        wx.login({
            success: function (login_res) {
                request({ url: "/guest/login/", data: { code: login_res.code, } })
                    .then((resp) => {
                        console.log(resp.open_id)
                        uni.setStorage({
                            key: 'my_open_id',
                            data: resp.open_id,
                            fail: function (res) { console.log(res) }
                        })
                        options.data.my_open_id = resp.open_id
                    })

            }
        })

    }
    return request(options)
}
export { registeredGuardRequest, registeredGuestRequest }
export default request