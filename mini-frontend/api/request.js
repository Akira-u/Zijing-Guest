function requestData(url, method = 'get', args = {}, header = {}) {
    if (!url) {
        console.warn("request empty url!")
    }
    return new Promise((resolve, reject) => {
        wx.request({
            url: url,
            data: args,
            header: header,
            method: method.toLocaleUpperCase(),
            success: function (res) {
                resolve(res);
            },
            fail: function (res) {
                reject(res.errMsg || '请求失败');
            }
        });
    });
}
export default requestData