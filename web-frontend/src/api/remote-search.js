import request from '@/utils/request'

export function searchUser(name) {
  return request({
    url: '/vue-element-admin/search/user',
    method: 'get',
    params: { name }
  })
}

export function transactionList(query) {
  return request({
    url: '/vue-element-admin/transaction/list',
    method: 'get',
    params: query
  })
}

export function getGuestStatic(query) {
  return request({
    url: 'http://49.232.106.46:8000/guest/static',
    method: 'get',
    params: query
  })
}
export function getGuardStatic(query) {
  return request({
    url: 'http://49.232.106.46:8000/guard/static',
    method: 'get',
    params: query
  })
}
export function getLogStatic(query) {
  return request({
    url: 'http://49.232.106.46:8000/log/static',
    method: 'get',
    params: query
  })
}
export function getDormStatic(query) {
  return request({
    url: 'http://49.232.106.46:8000/dorm/static',
    method: 'get',
    params: query
  })
}