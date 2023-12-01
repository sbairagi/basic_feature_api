from .views import FCMDeviceAuthorizedViewSet
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

# # Ifl Services Urls
# router.register('ifl-services/stocktips', IflServicesStockTipsViewSet)
# router.register('ifl-services/generic-notifications', IflServicesGenericNotificationViewSet)

# #Equity Global Urls
# router.register('equity-global/stocktips', EquityGlobalStockTipsViewSet)
# router.register('equity-global/generic-notifications', EquityGlobalGenericNotificationViewSet)

#Common Urls
router.register('list/devices', FCMDeviceAuthorizedViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
