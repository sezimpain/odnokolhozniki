from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from account.permissions import IsActive
from .models import Post
from .permissions import IsAuthorPermission
from .serializers import PostSerializer
from like.mixins import LikedMixin
from rest_framework.response import Response


class PermissionMixin:
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsActive]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthorPermission]
        else:
            permissions = [AllowAny]
        return [permission() for permission in permissions]


class MyPaginationClass(PageNumberPagination):
    # page_size = 3
    def get_paginated_response(self, data):
        for i in range(self.page_size):
             username = data[i]['username']
             data[i]['username'] = username[:9] + '...'
        return super().get_paginated_response(data)


class PostViewSet(PermissionMixin, ModelViewSet, LikedMixin):
    pagination_class = MyPaginationClass
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context


'''class BookmarkView(PermissionMixin, ModelViewSet,):
    model = Bookmark

    def post(self, request, pk):
        user = auth.get_user(request)
        bookmark, created = self.model.objects.get_or_create(user=user, obj_id = pk)
        # если не была создана новая закладка,
        # то считаем, что запрос был на удаление закладки
        if not created:
            bookmark.delete()'''


