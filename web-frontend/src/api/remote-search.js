import request from '@/utils/request'

export function getGuestStatic(query) {
  return request({
    url: '/guest/static',
    method: 'get',
    params: query
  })
}
export function getGuardStatic(query) {
  return request({
    url: '/guard/static',
    method: 'get',
    params: query
  })
}
export function getLogStatic(query) {
  return request({
    url: '/log/static',
    method: 'get',
    params: query
  })
}
export function getDormStatic(query) {
  return request({
    url: '/dorm/static',
    method: 'get',
    params: query
  })
}
