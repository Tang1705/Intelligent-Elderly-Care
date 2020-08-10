/*
 * @Description: 工具类
 * @Author: your name
 * @Date: 2019-07-30 11:40:12
 * @LastEditTime: 2019-12-01 23:43:20
 * @LastEditors: Please set LastEditors
 */
export function isvalidNull (str) {
    // 需要根据类型确定是否需要trim
    if (!str) return true // 排除Null
    else { // 排除空格
      str = str + ''
      if (str.trim().length < 1) {
        return true
      } else {
        return false
      }
    }
  }
  
  /**
   * @description: 判断输入的邮箱格式是否正确
   * @param {string}
   * @return: boolean（邮箱格式是否正确:false：格式错误）
   */
  export function isEmail (s) {
    return /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((.[a-zA-Z0-9_-]{2,3}){1,2})$/.test(s)
  }
  
  /**
   * @description: 判断输入的手机号是否正确
   * @param {string}
   * @return: boolean（手机号格式是否正确）
   */
  export function isMobile (s) {
    return /^1[3 4 5 7 8]\d{9}$/.test(s)
  }
  
  /**
   * @description: 判断输入的电话号码（座机号）是否正确
   * @param {string}
   * @return: boolean（电话号码格式是否正确）
   */
  export function isPhone (s) {
    // return /^([0-9]{3,4}-)?[0-9]{7,8}$/.test(s)
    return /^((0\d{2,3})-)?(\d{7,8})(-(\d{3,4}))?$/.test(s)
  }
  
  /**
   * @description: 判断输入的身份证号是否正确
   * 参考链接：https://www.jianshu.com/p/cbf4946c2b6d
   * @param {string}
   * @return: boolean（身份证号格式是否正确；false:身份证号格式错误）
   */
  export function isIDCard (s) {
    return /^(\d{15}$|^\d{18}$|^\d{17}(\d|X|x))$/.test(s)
  }
  
export const getBrowser = () => {
    let is_mobi = navigator.userAgent.toLowerCase().match(/(ipod|ipad|iphone|android|coolpad|mmp|smartphone|midp|wap|xoom|symbian|j2me|blackberry|wince)/i) != null;
    if (is_mobi) {
        return 'phone'
    }else{
        return  'pc'
    }
}