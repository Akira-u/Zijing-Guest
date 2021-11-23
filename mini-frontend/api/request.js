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
function requestData(options={}) {
    const {
        success,
        fail,
    } = options;
    if (!options.url) {
        console.warn("request empty url!")
    }
    return new Promise((res, rej) => {
        wx.request(Object.assign(
            {},
            options,
            {
                success(r) {
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
export default requestData