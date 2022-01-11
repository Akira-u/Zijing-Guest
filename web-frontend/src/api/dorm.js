import request from '@/utils/request'

export function getBuildingList(query) {
  return request({
    url: '/dormbuilding',
    method: 'get',
    params: query
  })
}
export function getDormList(query) {
  console.log(query)
  return request({
    url: '/dorm',
    method: 'get',
    params: query
  })
}
export function importList(data) {
  console.log(data)
  return request({
    url: '/dorm/bulk_create/',
    method: 'post',
    data
  })
}

