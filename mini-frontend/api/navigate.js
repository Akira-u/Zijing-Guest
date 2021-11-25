/**
* 包装好的uni.navigateTo(), 方便传参。
* 等价于"url?arg1=1&arg2=2..."
* 将参数内容全部用utf-8编码，适配&等特殊字符和长字符串
* 
* @param {string} url 要跳转到的页面相对路径/pages/xxx/xxx
* @param {object} args 参数对象
* @return {Function} uni.navigateTo({url:url?args.utf8})
*/
function navigateTo(url, args = {}) {
    if (args.constructor !== Object) {
        console.warn("wrong arg type: ", args.constructor)
        return uni.navigateTo({ url: url })
    }
    var str_arg=''
    for (var k in args) {
        let value = args[k] !== undefined ? args[k] : ''
        str_arg += k + '=' + encodeURIComponent(value) + '&'
    }
    url = str_arg ===''? url : url + "?" + str_arg.substr(0,str_arg.length-1)
    return uni.navigateTo({ url: url })
}

function reLaunch(url='/pages/index/index', args = {}) {
    if (args.constructor !== Object) {
        console.warn("wrong arg type: ", args.constructor)
        return uni.reLaunch({ url: url })
    }
    var str_arg = ''
    for (var k in args) {
        let value = args[k] !== undefined ? args[k] : ''
        str_arg += k + '=' + encodeURIComponent(value) + '&'
    }
    url = str_arg === '' ? url : url + "?" + str_arg.substr(0, str_arg.length - 1)
    console.log(url)
    return uni.reLaunch({ url: url })
}

function decodeOption(option) {
    for (var k in option) {
        option[k]=decodeURIComponent(option[k])
    }
}

export { decodeOption, reLaunch }
export default navigateTo;