from django.urls import path, include
from .views import *
from rest_framework import routers
from django.contrib.auth.views import (
    LogoutView, 
    # PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
router = routers.DefaultRouter()
router.register('signup', UserViewSet)

urlpatterns = [
     #Auth Urls
    path('', include(router.urls)),
    path("login/", ObtainTokenView.as_view(), name="Login"),
    # path('logout/', LogoutView.as_view(next_page='login'),name='logout'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),name='password_reset_complete'),
    path('password-reset/', PasswordResetView.as_view(),
        name='rest_password_reset'),
    path('change_password/', UpdatePassword.as_view(), name='auth_change_password'),
]
