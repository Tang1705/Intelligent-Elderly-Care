from .cookie import *
from .unjson import UnJson
from rest_framework.views import APIView
from rest_framework import status, generics
from django.http import Http404

import json

from ..models import oldperson_info, volunteer_info, employee_info
from ..serializer import OldPersonSerializer, VolunteerSerializer, EmployeeSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse


def checkToken(data):
    try:
        if check_token(data.token):
            return True
        else:
            res = {'code': 402, 'message': '请登入'}
            raise Http404(res)
    except BaseException:
        res = {'code': 402, 'message': '请登入'}
        raise Http404(res)


class oldManList(generics.ListCreateAPIView):
    """
    get:
    获取所有老人列表
    post：
    新加一个老人
    """
    queryset = oldperson_info.objects.all()
    serializer_class = OldPersonSerializer


class oldManDetail(APIView):
    """
    post:
    具体老人
    put:
    更新老人
    delete:
    删除老人
    """

    def get_object(self, pk):
        try:
            return oldperson_info.objects.get(pk=pk)
        except oldperson_info.DoesNotExist:
            raise Http404("不存在该老人")

    def post(self, request, formant=None):
        data = UnJson(request.data)
        checkToken(data)
        request.data.pop('token')
        oldMan = self.get_object(data.id)
        serializer = OldPersonSerializer(oldMan)
        return Response(serializer.data)

    def put(self, request, formant=None):
        data = UnJson(request.data)
        checkToken(data)
        request.data.pop('token')
        oldMan = self.get_object(data.id)
        serializer = OldPersonSerializer(oldMan,data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request, formant=None):
        data = UnJson(request.data)
        checkToken(data)
        request.data.pop('token')
        oldMan = self.get_object(data.id)
        oldMan.delete()
        return Response('老人删除成功', status=status.HTTP_204_NO_CONTENT)


class employeeList(generics.ListCreateAPIView):
    """
    get:
    获取所有员工列表
    post：
    新加一个员工
    """
    queryset = employee_info.objects.all()
    serializer_class = EmployeeSerializer


class employeeDetail(APIView):
    """
    post:
    具体员工
    put:
    更新员工
    delete:
    删除员工
    """

    def get_object(self, pk):
        try:
            return employee_info.objects.get(pk=pk)
        except employee_info.DoesNotExist:
            raise Http404("不存在该员工")

    def post(self, request, formant=None):
        data = UnJson(request.data)
        checkToken(data)
        request.data.pop('token')
        employee = self.get_object(data.id)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    def put(self, request, formant=None):
        data = UnJson(request.data)
        checkToken(data)
        request.data.pop('token')
        employee = self.get_object(data.id)
        serializer = OldPersonSerializer(employee,data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request, formant=None):
        data = UnJson(request.data)
        checkToken(data)
        request.data.pop('token')
        employee = self.get_object(data.id)
        employee.delete()
        return Response('员工删除成功', status=status.HTTP_204_NO_CONTENT)


class volunteerList(generics.ListCreateAPIView):
    """
    get:
    获取所有义工列表
    post：
    新加一个义工
    """
    queryset = volunteer_info.objects.all()
    serializer_class = VolunteerSerializer


class volunteerDetail(APIView):
    """
    post:
    具体义工
    put:
    更新义工
    delete:
    删除义工
    """

    def get_object(self, pk):
        try:
            return volunteer_info.objects.get(pk=pk)
        except volunteer_info.DoesNotExist:
            raise Http404("不存在该义工")

    def post(self, request, formant=None):
        data = UnJson(request.data)
        checkToken(data)
        request.data.pop('token')
        volunteer = self.get_object(data.id)
        serializer = VolunteerSerializer(volunteer)
        return Response(serializer.data)

    def put(self, request, formant=None):
        data = UnJson(request.data)
        checkToken(data)
        request.data.pop('token')
        volunteer = self.get_object(data.id)
        serializer = EmployeeSerializer(volunteer,data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request, formant=None):
        data = UnJson(request.data)
        checkToken(data)
        request.data.pop('token')
        volunteer = self.get_object(data.id)
        volunteer.delete()
        return Response('义工删除成功', status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def oldIDtoName(request,pk):
    """老人id换名字"""
    try:
        old = oldperson_info.objects.get(pk=pk)
    except oldperson_info.DoesNotExist:
        return HttpResponse(status=404)
    name=old.username
    return HttpResponse(name)


@api_view(['GET'])
def employeeIDtoName(request,pk):
    """义工id换名字"""
    try:
        employee = employee_info.objects.get(pk=pk)
    except employee_info.DoesNotExist:
        return HttpResponse(status=404)
    name=employee.username
    return HttpResponse(name)