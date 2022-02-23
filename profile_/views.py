from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from account.permissions import IsActive
from friend.mixins import FollowerMixin, FollowingMixin
from .serializers import ProfileSerializer, LocationSerializer
from .models import Profile, Location
from .permissions import IsAuthorPermission
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status, generics
from .services import LocationFilter


class PermissionMixin:
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsActive]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthorPermission]
        else:
            permissions = [AllowAny]
        return [permission() for permission in permissions]


class LocationListView(generics.ListAPIView, PermissionMixin):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class MyPaginationClass(PageNumberPagination):
    # page_size = 3
    def get_paginated_response(self, data):
        for i in range(self.page_size):
            bio = data[i]['bio']
            data[i]['bio'] = bio[:3] + '...'
        return super().get_paginated_response(data)


class ProfileViewSet(PermissionMixin, ModelViewSet, FollowerMixin, FollowingMixin):
    pagination_class = MyPaginationClass

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_class = LocationFilter

    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = self.queryset
        queryset = queryset.filter(Q(name__icontains=q))
        serializer = ProfileSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    @action(['GET'], detail=True)
    def reviews(self, request, pk=None):
        profile = self.get_object()
        reviews = profile.reviews.all()
        serializer = ProfileSerializer(
            reviews, many=True, context={'request': request}
        )
        return Response(serializer.data, status=200)

