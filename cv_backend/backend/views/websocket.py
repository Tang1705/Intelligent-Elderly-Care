import uuid
import json

from django.http import HttpResponse, JsonResponse, FileResponse
from dwebsocket.decorators import *
from rest_framework.decorators import api_view
from .unjson import UnJson

'''!------------------------WEBSOCKET--------------------------------!'''
clients = {}  # 创建客户端列表，存储所有在线客户端
cameras = {}  # 摄像头列表


# 网页websocket链接
@accept_websocket
def link(request):
    # 判断是不是ws请求
    if request.is_websocket():
        userid = str(uuid.uuid4())
        while True:
            message = request.websocket.wait()
            if not message:
                break
            else:
                print("客户端链接成功：" + str(message, encoding="utf-8"))
                # 保存客户端的ws对象，以便给客户端发送消息,每个客户端分配一个唯一标识
                clients[userid] = request.websocket


# 摄像头websocket链接
@accept_websocket
def cameraLink(request):
    # 判断是不是ws请求
    if request.is_websocket():
        userid = str(uuid.uuid4())
        while True:
            message = request.websocket.wait()
            if not message:
                break
            else:
                print("客户端链接成功：" + str(message, encoding="utf-8"))
                # 保存客户端的ws对象，以便给客户端发送消息,每个客户端分配一个唯一标识
                cameras[userid] = request.websocket


# 发送互动弹幕
def send(request):
    # 获取消息
    msg = request.POST.get("msg")
    # 获取到当前所有在线客户端，即clients
    # 遍历给所有客户端推送消息
    print('request:', request)
    print('request.data:', request.POST)
    if msg:
        for client in clients:
            clients[client].send(msg.encode('utf-8'))
        return HttpResponse({"msg": "success"})
    else:
        HttpResponse('发送格式错误')


def refresh():
    msg = 'refresh'
    for client in clients:
        clients[client].send(msg.encode('utf-8'))
    return HttpResponse('已让所有客户端刷新')


@api_view(['GET'])
def reboot(request):
    """
    重启
    :param request:
    :return:
    """
    msg = {
        'todo': 'reboot'
    }
    for camera in cameras:
        cameras[camera].send(json.dumps(msg, ensure_ascii=False))
    return HttpResponse('相机已重启')


@api_view(['POST'])
def entering(request):
    """
    录入信息
    id-人员id
    type-人员列表
    :param request:
    :return:
    """
    data = UnJson(request.data)
    msg = {
        'todo': 'entering',
        'data': {
            'id': data.id,
            'type': data.type
        }
    }

    for camera in cameras:
        cameras[camera].send(json.dumps(msg, ensure_ascii=False))
    return HttpResponse('相机已开始录制')


@api_view(['GET'])
def takePhoto(request):
    """
    拍照
    :param request:
    :return:
    """
    msg = {
        'todo': 'takePhoto',
        'data': {'fuc': 'shutter'}
    }
    for camera in cameras:
        cameras[camera].send(json.dumps(msg, ensure_ascii=False))
    return HttpResponse('相机已拍照')


@api_view(['GET'])
def standard(request):
    """
    拍照
    :param request:
    :return:
    """
    msg = {
        'todo': 'takePhoto',
        'data': {'fuc': 'standard'}
    }
    for camera in cameras:
        cameras[camera].send(json.dumps(msg, ensure_ascii=False))
    return HttpResponse('相机已标定')


@api_view(['POST'])
def changeFuc(request):
    """
    更改功能
    fuc:更改的功能 0:无 1微笑检测 2交互检测 3摔倒检测 4禁区入侵
    :param request:
    :return:
    """
    data = UnJson(request.data)
    print(data.fuc)
    msg = {
        'todo': 'change',
        'data': {'fuc': data.fuc}
    }
    print(msg)

    for camera in cameras:
        cameras[camera].send(json.dumps(msg, ensure_ascii=False))
    return HttpResponse('相机功能已更改')


@api_view(['POST'])
def totalNum(request):
    data = UnJson(request.data)
    msg = {
        'elderNum': data.old,
        'staffNum': data.employee,
        'volunteerNum': data.volunteer,
        'strangerNum': data.stranger
    }
    for client in clients:
        clients[client].send(json.dumps(msg, ensure_ascii=False))
    return HttpResponse("success")
