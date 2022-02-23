from rest_framework.response import Response
from friend import services
from .serializers import FollowingSerializer, FollowerSerializer
from rest_framework.decorators import action


class FollowingMixin:
    @action(methods=['POST'], detail=True)
    def following(self, request, pk=None):
        obj = self.get_object()
        services.add_following(obj, request.user)
        return Response()

    @action(methods=['POST'], detail=True)
    def unfollowing(self, request, pk=None):
        obj = self.get_object()
        services.remove_following(obj, request.user)
        return Response()

    @action(methods=['GET'], detail=True)
    def followers(self, request, pk=None):
        obj = self.get_object()
        followers = services.get_followers(obj)
        serializer = FollowerSerializer(followers, many=True)
        return Response(serializer.data)


class FollowerMixin:
    @action(methods=['GET'], detail=True)
    def followings(self, request, pk=None):
        obj = self.get_object()
        following = services.get_following(obj)
        serializer = FollowerSerializer(following, many=True)
        return Response(serializer.data)
