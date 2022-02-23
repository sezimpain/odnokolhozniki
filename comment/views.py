from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Comment, ReplyComment, Bookmark
from .serializers import CommentSerializer, ReplyCommentSerializer, BookmarkSerializer
from post.views import PermissionMixin


class CommentViewSet(PermissionMixin, ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context

    @action(detail=False, methods=['get'])
    def bookmarks(self, request):
        queryset = Bookmark.objects.all()
        queryset = queryset.filter(username=request.user)
        serializer = BookmarkSerializer(
            queryset,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'],
            permission_classes=[IsAuthenticated]
            )
    def bookmark(self, request, pk=None):
        comment = self.get_object()
        obj, created = Bookmark.objects.get_or_create(
            username=request.user,
            comment=comment
        )
        if not created:
            obj.favorite = not obj.favorite
            obj.save()
        favorites = 'Added to favorites' if obj.favorite else 'Removed from favorites'

        return Response('{}!'.format(favorites), status=status.HTTP_200_OK)


class ReplyCommentViewSet(PermissionMixin, ModelViewSet):
    queryset = ReplyComment.objects.all()
    serializer_class = ReplyCommentSerializer
