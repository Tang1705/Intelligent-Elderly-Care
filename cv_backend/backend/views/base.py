from .cookie import *
from .unjson import UnJson
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404

import json

from ..models import sys_user, Account
from ..serializer import SysUserSerializer, AccountSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse


@api_view(['POST'])
def LoginIn(request):
    """
    登录
    :param request:
    {username}账户名
    :return:
    """
    data = UnJson(request.data)
    print(data)
    try:
        user = Account.objects.filter(username=data.username, password=data.password)
        if user:
            data = {'code': 200, 'token': create_token(data.username), 'message': 'sendsuceed', }
            response = HttpResponse(json.dumps(data))
            # response.set_cookie("token", create_token(data.account), 1800)
            response.status_code = 200
            print(response)
            return response
    except IOError:
        print('2333')
    else:
        data = {'code': 403, 'message': '用户名或密码错误'}
        response = HttpResponse(json.dumps(data))
        print('用户名或密码错误')
        return response


class AccountDetail(APIView):
    """
    post:
    注册账户

    put:
    修改密码
    """

    def checkToken(self, data):
        try:
            if check_token(data.token):
                return True
            else:
                print('token无效')
                res = {'code': 402, 'message': '请登入'}
                raise Http404(res)
        except BaseException:
            print('无token')
            res = {'code': 402, 'message': '请登入'}
            raise Http404(res)

    def post(self, request, formant=None):

        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            a = serializer.save()  # 顺便添加一个资料对象
            user = sys_user(account=a)
            user.save()
            res = {'code':200,'token': create_token(a.username),'message':'注册成功'}
            return HttpResponse(json.dumps(res,ensure_ascii=False))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        data = UnJson(request.data)
        # print(data)
        self.checkToken(data)
        try:
            user = Account.objects.get(pk=data.username)
        except Account.DoesNotExist:
            raise Http404

        # print(user)
        if data.oldPassword == user.password:
            pass
        else:
            return HttpResponse(json.dumps({'msg':'原密码错误'}, ensure_ascii=False))
        serializer = AccountSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(json.dumps({'msg':'修改成功','code':200}, ensure_ascii=False))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SysUserDetail(APIView):
    """
    获取个人资料信息
    post:
    获取

    put:
    更新资料

    """
    def checkToken(self, data):
        try:
            if check_token(data.token):
                return True
            else:
                print('token无效')
                res = {'code': 402, 'message': '请登入'}
                raise Http404(res)
        except BaseException:
            res = {'code': 402, 'message': '请登入'}
            raise Http404(res)

    def getInfo(self,username):
        try:
            user = Account.objects.get(pk=username)
            user_info = sys_user.objects.get(pk=user)
            return user, user_info
        except Account.DoesNotExist or sys_user.DoesNotExist:
            raise Http404('账户不合法')

    def post(self, request, formant=None):
        data = UnJson(request.data)
        user, user_info = self.getInfo(data.username)
        serializer = SysUserSerializer(user_info)
        return Response(serializer.data)

    def put(self,request, formant=None):
        data = UnJson(request.data)
        # self.checkToken(data)
        print(request.data)

        user, user_info = self.getInfo(data.account)

        # print(request.data['account'])
        serializer = SysUserSerializer(user_info,data=request.data)
        if serializer.is_valid():
            serializer.validated_data['account'] = user
            serializer.save()
            return HttpResponse(json.dumps({'code':200,'mes':'修改成功'},ensure_ascii=False))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

