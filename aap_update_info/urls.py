from .views import UpdateinfoViewSet
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register('', UpdateinfoViewSet)

urlpatterns = [
    path('', include(router.urls))
]