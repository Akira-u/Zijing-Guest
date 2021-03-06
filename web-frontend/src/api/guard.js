import request from '@/utils/request'

export function getList(query) {
  return request({
    url: '/guard/',
    method: 'get',
    params: query
  })
}

export function editBuilding(query) {
  const data = { open_id: query.open_id, dormbuilding_id: query.building_id }
  return request({
    url: '/guard/' + query.open_id + '/',
    method: 'patch',
    data
  })
}

export function preCreate(data) {
  return request({
    url: '/guard/pre_create/',
    method: 'post',
    data
  })
}

export function del(open_id) {
  return request({
    url: 'https://c02.whiteffire.cn:8000/guard/' + open_id + '/',
    method: 'delete'
  })
}
