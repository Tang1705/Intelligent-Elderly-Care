export default {
  /**
  * 测试
  * */
  baseURL: 'http://192.144.229.49:8000/api/',
  // baseURL: 'http://127.0.0.1:8000/api/',
  qianduanURL: 'http://59.64.3.20:8088',
  uploadURL: 'http://192.144.229.49:8000/api/base/upload/avatar',
  imageURL:'http://192.144.229.49:8000/api/base/getPhoto/',


  method: 'post',

  /**
   * 基本
   */
  login:{url:'login'},
  signUp:{url:'account'},
  setInfo:{url:'base/sysInfo'},

  /**
   * 人员管理
   */
  oldPersonList:{url:'person/oldManList'},
  oldPersonDetail:{url:'person/oldManDetail'},
  employeeList:{url:'person/employeeList'},
  employeeDetail:{url:'person/employeeDetail'},

  volunteerList:{url:'person/volunteerList'},
  volunteerDetail:{url:'person/volunteerDetail'},

  /**
   * 实时事件
   */
  eventList:{url:'event/list'},

  /**
   * 统计报表
   */
  peopleCount:{url:'/statistics/all'},
  eventCount:{url:'/statistics/dailyEvent'},
  oldAnalysis:{url:'statistics/oldAnalysis'},
  communicateOld :{url:'statistics/communicateOld '},
  smileOld:{url:'statistics/smileOld'},
  age:{url:'statistics/age'},

  /**
   * Websocket
   */
  entering:{url:'websocket/entering'},
  reboot:{url:'websocket/reboot'},
  changeFuc:{url:'websocket/changeFuc'},
  takePhoto:{url:'websocket/takePhoto'},
  standard:{url:'websocket/standard'}

}
