import request from '@/utils/request'

export function getList(query) {
  return request({
    url: 'https://c02.whiteffire.cn:8000/log',
    method: 'get',
    params: query
  })
}
