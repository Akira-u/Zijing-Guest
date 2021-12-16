import request from '@/utils/request'

export function getList(query) {
  return request({
    url: '/guest',
    method: 'get',
    params: query
  })
}

export function getLog(query) {
  return request({
    url: '/log',
    method: 'get',
    params: query
  })
}

export function toBlackList(data) {
  console.log(data)
  return request({
    url: '/guest/to_black/',
    method: 'post',
    data
  })
}

export function toWhiteList(data) {
  return request({
    url: '/guest/to_white/',
    method: 'post',
    data
  })
}
