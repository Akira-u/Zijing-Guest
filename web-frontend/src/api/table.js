import request from '@/utils/request'

export function getList(query) {
  return request({
    url: 'http://49.232.106.46:8000/log',
    method: 'get',
    params: query
  })
}
