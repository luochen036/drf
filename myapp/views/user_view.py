from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from myapp.models import UserInfo
from myapp.serializers import user_serializer as user_sers
from myapp.extension.mixins import MyCreateModelMixin
import uuid
from datetime import datetime, timedelta


# 注册视图
class RegisterView(MyCreateModelMixin, GenericViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = user_sers.RegisterSerializer

    def perform_create(self, serializer):
        serializer.validated_data.pop('re_password')
        serializer.save()


# 认证视图
class AuthView(APIView):

    def post(self, request, *args, **kwargs):
        # 校验参数
        ser = user_sers.AuthSerializer(data=request.data)
        if not ser.is_valid():
            return Response({'code': 400, 'msg': '数据校验失败', 'errors': ser.errors}, status=400)

        username = ser.validated_data.get('username')
        phone = ser.validated_data.get('phone')
        password = ser.validated_data.get('password')

        if not UserInfo.objects.filter(Q(username=username) | Q(phone=phone)).exists():
            return Response({'code': 400, 'msg': '用户名或手机号不存在'}, status=400)
        user = UserInfo.objects.filter(Q(username=username) | Q(phone=phone)).first()
        if user.password != password:
            return Response({'code': 400, 'msg': '密码错误'}, status=400)

        token = str(uuid.uuid4())
        user.token = token
        # 过期时间设置为1天后
        user.token_expire = datetime.now() + timedelta(days=1)
        user.save()
        return Response({'code': 200, 'msg': '认证成功', 'data':
                         {'token': token, 'username': user.username}
                         }, status=200)
