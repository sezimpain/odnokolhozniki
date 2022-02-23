from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet  # ReplyPostViewSet

router = DefaultRouter()
#router.register('post_reply', ReplyPostViewSet)
router.register('post', PostViewSet)
urlpatterns = [
    path("", include(router.urls)),
]