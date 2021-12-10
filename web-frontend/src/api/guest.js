import request from '@/utils/request'

export function getList(query) {
  return request({
    url: 'http://49.232.106.46:8000/guest',
    method: 'get',
    params: query
  })
}

export function getLog(query) {
  return request({
    url: 'http://49.232.106.46:8000/log',
    method: 'get',
    params: query
  })
}

export function toBlackList(data) {
  console.log(data)
  return request({
    url: 'http://49.232.106.46:8000/guest/to_black/',
    method: 'post',
    data
  })
}

export function toWhiteList(data) {
  return request({
    url: 'http://49.232.106.46:8000/guest/to_white/',
    method: 'post',
    data
  })
}
