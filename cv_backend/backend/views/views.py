from django.shortcuts import render
from .cookie import *
import datetime
from .unjson import UnJson
from rest_framework.views import APIView
from rest_framework import status, generics
from django.http import Http404

import json

from ..models import oldperson_info, volunteer_info, employee_info, event_info
from ..serializer import OldPersonSerializer, VolunteerSerializer, EmployeeSerializer, EventSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse


# Create your views here.


@api_view(['POST'])
def uploadAvatar(request):
    """
    上传接口 type：0 代表老人 1 代表工作人员 2 代表义工
    :param request:
    :return:
    """
    upload_file = request.FILES['file']
    request.data.pop('file')
    data = UnJson(request.data)
    obj = ''
    try:
        type = data.type
        id = data.id
    except BaseException:
        return HttpResponse('type 和 id 为必填字段 0 代表老人 1 代表工作人员 2 代表义工')

    try:
        print(id)
        if type == '0':
            type = "oldperson"
            obj = oldperson_info.objects.get(pk=id)
            serializer = OldPersonSerializer(obj)
        elif type == '1':
            type = "employee"
            obj = employee_info.objects.get(pk=id)
            serializer = EmployeeSerializer(obj)
        elif type == '2':
            type = "volunteer"
            obj = volunteer_info.objects.get(pk=id)
            serializer = VolunteerSerializer(obj)
        else:
            return HttpResponse('type 和 id 为必填字段 0 代表老人 1 代表工作人员 2 代表义工')
    except  employee_info.DoesNotExist or oldperson_info.DoesNotExist or volunteer_info.DoesNotExist:
        return HttpResponse('找不到该' + type)

    print(upload_file)
    url = './img/avatar/' + type + id + '-av-' + upload_file.name
    file = open(url, 'wb+')
    for chunk in upload_file.chunks():
        file.write(chunk)

    obj.profile_photo = url
    obj.save()
    # if serializer.is_valid():
    #     serializer.validated_data['profile_photo'] = url
    #     serializer.save()

    return Response(serializer.data)


# 获取照片，id为imgid
@api_view(['GET'])
def getImg(request, id):
    result = id
    print(result)
    path = './'+result
    image_data = open(path, "rb").read()
    return HttpResponse(image_data, content_type="image/jpg")