from django.urls import path
from rest_framework import routers
from .views import user_view, topic_view
from django.conf import settings
from django.conf.urls.static import static

# 创建路由对象
router = routers.SimpleRouter()
# 注册路由
router.register(r"register", user_view.RegisterView, basename="register")
router.register(r"topic", topic_view.TopicView, basename="topic")

urlpatterns = [
    path('auth/', user_view.AuthView.as_view(), name='auth'),
]

urlpatterns += router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
