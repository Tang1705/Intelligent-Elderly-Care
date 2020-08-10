/*
 * 全局状态
 */
import Vue from 'vue'
import Vuex from 'vuex'
import Cookie from 'cookie'
import Cookies from 'js-cookie'
import API from '../api'
import _ from 'lodash'

Vue.use(Vuex)
const cookieTokenName = 'token'
const cookieTokenExpiredName = 'token_expired'
const cookieType = 'type'
const cookieUserName = 'user'
const isBrowser = process.browser

export const state = () => ({
  tdk: {},
  type: 0,
  info:{}
})

export const mutations = {
  SET_TOKEN (state, token) {
    token = token || ''
    state.token = token
    if (token && isBrowser) {
      Cookies.set(cookieTokenName, token)
    }
  },
  // 将数据存储在cookie和store中
  /**
   * 0是普通用户，1是管理员
   * */
  SET_TYPE (state, type) {
    type = type || 0
    state.type = type
    Cookies.set(cookieType, type)
  },
  SET_TOKEN_EXPIRED (state, expired) {
    state.tokenExpired = expired
    if (expired && isBrowser) {
      Cookies.set(cookieTokenExpiredName, expired)
    }
  },
  SET_USER (state, user) {
    user = user || {}
    state.user = _.isObject(user) ? user : JSON.parse(user)
    if (user && isBrowser) {
      Cookies.set(cookieUserName, user)
    }
  },
  // 将登录返回的info对象存储
  SET_INFO (state, info) {
    info = info || {}
    state.info = _.isObject(info) ? info : JSON.parse(info)
    Cookies.set('info', info)
  }
}

export const actions = {
  async nuxtClientInit ({commit}, context) {
    await context.store.dispatch('auth/load_token', context)
    await context.store.dispatch('auth/load_user', context)
  },
  async load_token ({commit}, {req}) {
    const cookieStr = isBrowser ? document.cookie : req.headers.cookie
    const cookies = Cookie.parse(cookieStr || '') || {}
    commit('SET_TOKEN', cookies[cookieTokenName])
    commit('SET_TOKEN_EXPIRED', cookies[cookieTokenExpiredName])
  },
  async check_token_expired ({commit, state, dispatch}) {
    let token = state.token
    let tokenExpired = state.tokenExpired
    let timestamp = parseInt(Date.now() / 1000)

    return token && tokenExpired > 0 && tokenExpired - timestamp < 1
  },
  async load_user ({commit}, {req}) {
    const cookieStr = isBrowser ? document.cookie : req.headers.cookie
    const cookies = Cookie.parse(cookieStr || '') || {}
    commit('SET_USER', cookies[cookieUserName])
  },
  async auth_success ({commit, dispatch}, res) {
    commit('SET_TOKEN', res.token)
//将返回的用户info信息保存到全局状态和cookie中
    commit('SET_TYPE', res.type)
    commit('SET_INFO', res.info)
    commit('SET_TOKEN_EXPIRED', parseInt(res.expired) + parseInt(Date.now() / 1000))
  },
  async login ({commit, dispatch}, data) {
    let result = -1
    await API.loginApi(data).then(res => {
      if (res.code === undefined) {
        dispatch('auth_success', res)
      }
      result = res
    })
    return result
  },
  async misLogin ({commit, dispatch}, data) {
    let result = -1
    await API.misLogin(data).then(res => {
      if (res.code === undefined) {
        dispatch('auth_success', res)
      }
      result = res
    })
    return result
  },
  // async logout ({commit}, data) {
  //   let result = false
  //   await API.logoutApi(data).then(res => {
  //     result = res.status
  //     if (result) {
  //       commit('SET_TOKEN', '')
  //       commit('SET_TOKEN_EXPIRED', 0)
  //       commit('SET_USER', {})
  //       Cookies.remove(cookieTokenName)
  //       Cookies.remove(cookieTokenExpiredName)
  //       Cookies.remove(cookieUserName)
  //     }
  //   })
  // }
}
