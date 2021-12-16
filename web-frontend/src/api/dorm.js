import request from '@/utils/request'

export function getBuildingList(query) {
  return request({
    url: 'https://c02.whiteffire.cn:8000/dormbuilding',
    method: 'get',
    params: query
  })
}
export function getDormList(query) {
  console.log(query)
  return request({
    url: 'https://c02.whiteffire.cn:8000/dorm',
    method: 'get',
    params: query
  })
}
export function importList(data) {
  console.log(data)
  return request({
    url: 'https://c02.whiteffire.cn:8000/dorm/bulk_create/',
    method: 'post',
    data
  })
}

