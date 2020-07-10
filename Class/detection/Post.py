import requests
import datetime

url = "http://192.144.229.49:8000/api/event/list"

data_type_one = {
    "oldperson_id": 1,
    "event_type": 3,  # 0代表情感检测，1代表义工交互检测，2代表陌生人检测，3代表摔倒检测，4代表禁止区域入侵检测
    "event_date": "",  # 事件日期
    "event_location": "",  # 事件地点(选)
    "event_desc": ""  # 必填,事件描述

}

data_type_two = {
    "event_type": 3,  # 0代表情感检测，1代表义工交互检测，2代表陌生人检测，3代表摔倒检测，4代表禁止区域入侵检测
    "event_date": "",  # 事件日期
    "event_location": "",  # 事件地点(选)
    "event_desc": ""  # 必填,事件描述
}


def post(elder_id='None', event=-1, imagePath='None', volunteer='None'):
    flag = 0
    if event == 0:
        data_type_one['oldperson_id'] = elder_id
        data_type_one['event_type'] = event
        data_type_one['event_date'] = datetime.datetime.today().date()
        data_type_one['event_location'] = '来自房间的摄像头'
        data_type_one['event_desc'] = '老人笑了'
        flag = 1
    elif event == 1:
        data_type_one['oldperson_id'] = elder_id
        data_type_one['event_type'] = event
        data_type_one['event_date'] = datetime.datetime.today().date()
        data_type_one['event_location'] = '来自桌子上的摄像头'
        data_type_one['event_desc'] = '老人与' + volunteer + '交互了'
        flag = 1
    elif event == 2:
        data_type_two['event_type'] = event
        data_type_two['event_date'] = datetime.datetime.today().date()
        data_type_two['event_location'] = '来自房间的摄像头'
        data_type_two['event_desc'] = '有陌生人出现在房间了'
        flag = 2
    elif event == 3:
        data_type_two['event_type'] = event
        data_type_two['event_date'] = datetime.datetime.today().date()
        data_type_two['event_location'] = '来自走廊的摄像头'
        data_type_two['event_desc'] = '老人摔倒了'
        flag = 2
    elif event == 4:
        data_type_two['event_type'] = event
        data_type_two['event_date'] = datetime.datetime.today().date()
        data_type_two['event_location'] = '来自院子的摄像头'
        data_type_two['event_desc'] = '有人闯入禁止区域了'
        flag = 2

    file = open(imagePath, 'rb')
    imageFile = {'file': file}
    if flag == 1:
        status = requests.post(url, files=imageFile, data=data_type_one)
    else:
        status = requests.post(url, files=imageFile, data=data_type_two)
    print(status)
