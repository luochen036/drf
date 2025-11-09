import django_filters
from myapp.extension.mixins import MyCreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from myapp.models import Topic, UserInfo
from myapp.serializers.topic_serializer import TopicSerializer
from rest_framework.filters import BaseFilterBackend
from django_filters.rest_framework import DjangoFilterBackend, FilterSet

# 自定义filter
class MyTopicFilter(BaseFilterBackend):
    # 重写核心方法
    def filter_queryset(self, request, queryset, view):
        # 自定义过滤逻辑
        # 例如，根据用户是否登录来过滤
        queryset = queryset.filter(user=request.user)
        return queryset


# 自定义filterset
class MyTopicFilterset(FilterSet):
    min_id = django_filters.NumberFilter(field_name="id", lookup_expr="gte")  # 大于等于min_id
    order_by = django_filters.OrderingFilter(fields=["id", "create_time"])  # 排序字段

    class Meta:
        model = Topic
        fields = ["id", "create_time"]


class TopicView(MyCreateModelMixin, GenericViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    filter_backends = [MyTopicFilter, DjangoFilterBackend]
    filterset_class = MyTopicFilterset

    # 重写perform_create方法，在保存时添加user字段
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
