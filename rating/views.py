from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from post.views import PermissionMixin
from rating.models import Rating
from rating.serializers import RatingSerializer


class RatingViewSet(ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


