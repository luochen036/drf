"""
    自定义的Mixin类：
        继承五大类，做自己的封装，重写create方法
"""
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response


# 做一层封装，进行拓展
class MyCreateModelMixin(CreateModelMixin):
    # 重写create方法 对应http post请求
    def create(self, request, *args, **kwargs):
        # 默认是有继承GenericViewSet的，所以可以直接调用get_serializer方法
        # 拿到视图中定义的序列化器对象
        ser = self.get_serializer(data=request.data)
        if not ser.is_valid():
            return Response({'code': 400, 'msg': '数据校验失败', 'errors': ser.errors}, status=400)
        # 通过调用perform_create方法，完成数据的保存
        self.perform_create(ser)
        return Response({'code': 201, 'msg': '注册成功', 'data': ser.data}, status=201)

    def list(self, request, *args, **kwargs):
        # 从数据库中查询所有的话题
        # self.get_queryset()  拿到类中定义的查询集
        # self.filter_queryset()  过滤器过滤一层数据集
        queryset = self.filter_queryset(self.get_queryset())
        # page分页器对象，表示分页后的数据集
        page = self.paginate_queryset(queryset)
        # 如果有page数据集，说明进行了分页
        if page is not None:
            # 对page进行序列化
            serializer = self.get_serializer(page, many=True)
            # 正常：Response(serializer.data)
            # self.get_paginated_response  分页器的方法，对分页后的数据集进行封装
            return self.get_paginated_response(serializer.data)
        # 将queryset数据集，进行序列化
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)