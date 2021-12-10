import request from '@/utils/request'

export function getBuildingList(query) {
  return request({
    url: 'http://49.232.106.46:8000/dormbuilding',
    method: 'get',
    params: query
  })
}
export function getDormList(query) {
  console.log(query)
  return request({
    url: 'http://49.232.106.46:8000/dorm',
    method: 'get',
    params: query
  })
}

// export function toWhiteList(data) {
//     return request({
//       url: 'http://49.232.106.46:8000/guest/to_white/',
//       method: 'post',
//       data
//     })
//   }
