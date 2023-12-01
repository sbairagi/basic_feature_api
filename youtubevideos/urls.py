from django.urls import path, include
from rest_framework import routers
from .views import YouubeVideosViewSet

router = routers.DefaultRouter()
router.register('videos', YouubeVideosViewSet)

urlpatterns = [
    path('', include(router.urls)),
]