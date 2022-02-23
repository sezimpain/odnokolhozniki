from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommentViewSet, ReplyCommentViewSet
router = DefaultRouter()
router.register('comment', CommentViewSet)
router.register('comment_reply', ReplyCommentViewSet)
urlpatterns = [
    path('', include(router.urls))
]
