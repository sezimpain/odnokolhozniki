from rest_framework.routers import DefaultRouter

from rating.views import RatingViewSet
from django.urls import path, include
router = DefaultRouter()
router.register('rating', RatingViewSet)
urlpatterns = [
    path('', include(router.urls))
]
