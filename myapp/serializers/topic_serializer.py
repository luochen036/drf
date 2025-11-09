from rest_framework import serializers
from myapp.models import Topic
from rest_framework import exceptions


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ["id", "name", "is_hot"]
        extra_kwargs = {
            "is_hot": {"read_only": True}  # 只需要参与序列化，不需要写入
        }
