from rest_framework import serializers
from rest_framework import exceptions
from myapp.models import UserInfo


# 注册序列化器
class RegisterSerializer(serializers.ModelSerializer):
    # 确认密码，只需要校验，不参与序列化
    re_password = serializers.CharField(write_only=True, min_length=6, max_length=32)

    # 元类
    class Meta:
        model = UserInfo
        fields = ["username", "password", "phone", "re_password"]

        extra_kwargs = {
            "username": {"min_length": 2, "max_length": 10, 'error_messages': {
                "min_length": "用户名不能少于2个字符",
                "max_length": "用户名不能超过10个字符"
            }},
            "password": {"write_only": True, "min_length": 6, "max_length": 32, 'error_messages': {
                "min_length": "密码不能少于6个字符",
                "max_length": "密码不能超过32个字符"
            }},
            "phone": {"min_length": 11, "max_length": 11
                , 'error_messages': {
                    "min_length": "手机号只能11个字符",
                    "max_length": "手机号只能11个字符"
                }}
        }

    # 用户名钩子
    def validate_username(self, username):
        # 检查用户名是否重复
        if UserInfo.objects.filter(username=username).exists():
            raise serializers.ValidationError('用户名已经存在')
        return username

    # 手机号钩子
    def validate_phone(self, phone):
        # 判断字符串是否为1开头
        if not phone.startswith('1'):
            raise serializers.ValidationError('手机号必须以1开头')
        # 手机号不能重复
        if UserInfo.objects.filter(phone=phone).exists():
            raise serializers.ValidationError('手机号已经存在')

        return phone

    # 检查2次密码是否一致
    def validate(self, attrs):
        print(attrs)
        # attrs是校验后的数据字典
        # 检查2次密码是否一致
        password = attrs.get('password')
        re_password = attrs.get('re_password')
        if password != re_password:
            raise serializers.ValidationError({"re_password": "两次密码不一致"})
        return attrs


# 认证序列化器
class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=10, min_length=2, required=False)
    phone = serializers.CharField(max_length=11, min_length=11, required=False)
    # 密码只需要校验，不参与序列化
    password = serializers.CharField(max_length=32, min_length=6, write_only=True)

    # 全局校验方法
    def validate(self, attrs):
        username = attrs.get('username')
        phone = attrs.get('phone')
        password = attrs.get('password')
        # 校验用户名和手机号是否同时存在
        if not username and not phone:
            raise serializers.ValidationError({'username': '用户名和手机号不能均为空'})
        # 检验用户名和手机号是否同时存在
        if username and phone:
            raise serializers.ValidationError({'username': '用户名和手机号不能同时存在'})
        # 校验密码是否存在
        if not password:
            raise serializers.ValidationError({'password': '密码不能为空'})
        return attrs
