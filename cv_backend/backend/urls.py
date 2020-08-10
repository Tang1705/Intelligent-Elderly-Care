from django.conf.urls import url
from rest_framework.documentation import include_docs_urls
from .views import base, person, statistics, views, websocket

urlpatterns = [

    url('docs/', include_docs_urls(title='API接口文档')),

    # BASE 基本
    url('login', base.LoginIn),
    url('account', base.AccountDetail.as_view()),
    url('base/sysInfo', base.SysUserDetail.as_view()),

    # url('base/changeNotify', ),
    # url('base/entryFace', ),
    # url('base/webSocket'),
    url('base/upload/avatar', views.uploadAvatar),
    # url('base/upload/event', ),
    url('base/getPhoto/(?P<id>.+)/$', views.getImg),

    # PERSONAL MANAGEMENT 人员管理

    #   Old Man  老人
    url('person/oldManList', person.oldManList.as_view()),
    url('person/oldManDetail', person.oldManDetail.as_view()),
    url('person/old/(?P<pk>[0-9]+)/$', person.oldIDtoName),
    #   Employee  员工
    url('person/employeeList', person.employeeList.as_view()),
    url('person/employeeDetail', person.employeeDetail.as_view()),
    #   Volunteer  义工
    url('person/volunteerList', person.volunteerList.as_view()),
    url('person/volunteerDetail', person.volunteerDetail.as_view()),
    url('person/employee/(?P<pk>[0-9]+)/$', person.oldIDtoName),

    # EVENT 事件
    url('event/list', statistics.eventList.as_view()),

    # STATISTICS 统计报表
    url('statistics/all', statistics.allTotal),  # 所有人员的统计
    url('statistics/excel', statistics.exportExcel),  # 导出excel
    url('statistics/age', statistics.oldManAge),  # 按老人年龄区间
    url('statistics/event', statistics.todayEvent),  # 一周五个时事件总和
    url('statistics/dailyEvent', statistics.dailyEvent),  # 事件走势
    url('statistics/smileOld', statistics.smileStar),  # 微笑之星
    url('statistics/communicateOld', statistics.communicateStar),  # 交际之星
    url('statistics/oldAnalysis', statistics.oldAnalysis),  # 老人分析

    # WEBSOCKET
    url('websocket/link', websocket.link),
    url('websocket/send', websocket.send),
    url('websocket/refresh', websocket.refresh),
    url('websocket/cameraLink', websocket.cameraLink),
    url('websocket/reboot', websocket.reboot),
    url('websocket/entering', websocket.entering),
    url('websocket/changeFuc', websocket.changeFuc),
    url('websocket/takePhoto', websocket.takePhoto),
    url('websocket/standard', websocket.standard),
    url('websocket/total', websocket.totalNum),


]
