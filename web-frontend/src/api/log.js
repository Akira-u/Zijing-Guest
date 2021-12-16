import request from '@/utils/request'

export function getList(query) {
  return request({
    url: '/log',
    method: 'get',
    params: query
  })
}
