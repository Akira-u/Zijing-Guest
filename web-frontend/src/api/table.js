import request from '@/utils/request'

export function getList(params) {
  return request({
    url: 'http://c02.whiteffire.cn:8000/log',
    method: 'get',
    params
  })
}
