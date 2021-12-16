import request from '@/utils/request'

export function adminLogin(data) {
  return request({
    url: 'http://49.232.106.46:8000/guard/admin_login/',
    method: 'post',
    data
  })
}

export function login(data) {
  return request({
    url: '/vue-admin-template/user/login',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    url: '/vue-admin-template/user/info',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    url: '/vue-admin-template/user/logout',
    method: 'post'
  })
}
