from datetime import datetime

from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

from myapp.models import UserInfo


# 登录认证类
class tokenAuth(BaseAuthentication):
    def authenticate(self, request):
        token = request.data.get('token')
        if not token:
            raise exceptions.AuthenticationFailed({'code': 400, 'msg': 'token为空'})
        user = UserInfo.objects.filter(token=token).first()
        if not user:
            raise exceptions.AuthenticationFailed({'code': 400, 'msg': 'token错误'})
        if user.token_expire < datetime.now():
            raise exceptions.AuthenticationFailed({'code': 400, 'msg': 'token过期'})
        return user, token
