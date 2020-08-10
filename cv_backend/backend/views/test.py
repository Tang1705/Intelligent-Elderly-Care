import requests
from websocket import create_connection

def sendEvent():
    url = "http://192.144.229.49:8000/api/event/list"

    imagePath = 'train.jpg'

    data = {
        "oldperson_id": 1,
        "event_type": 0,  # 0代表情感检测，1代表义工交互检测，2代表陌生人检测，3代表摔倒检测，4代表禁止区域入侵检测
        "event_date": "2020-07-06",  # 事件日期
        "event_location": "",  # 事件地点(选)
        "event_desc": "老人笑了ba???"  # 必填,事件描述
    }

    file = open(imagePath, 'rb')

    imageFile = {'file': file}

    requests.post(url, files=imageFile, data=data)

