import request from '@/utils/request'

export function login(data) {
  return request({
    url: 'http://0.0.0.0:8000/auth/',
    method: 'get',
    data
  })
}

export function getInfo(token) {
  return request({
    url: '/user/info',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    url: '/user/logout',
    method: 'post'
  })
}
