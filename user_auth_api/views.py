from django.contrib.auth import get_user_model
from rest_framework import views, permissions, status
from rest_framework.response import Response
from rest_framework import viewsets

from .serializers import ChangePasswordSerializer, ObtainTokenSerializer, UserSerializer 
from .authentication import JWTAuthentication


from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordContextMixin
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth import (
    get_user_model, login as auth_login
)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .serializers import PasswordResetSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics

# Create your views here.

User = get_user_model()

# login
class ObtainTokenView(views.APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ObtainTokenSerializer

    def post(self, request, *args, **kwargs):
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email_or_phone_number = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user = User.objects.filter(email=email_or_phone_number).first()
        if user is None:
            user = User.objects.filter(phone_number=email_or_phone_number).first()

        if user is None or not user.check_password(password):
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate the JWT token
        jwt_token = JWTAuthentication.create_jwt(user)

        return Response({'token': jwt_token})
    

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Permissions
    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'retrieve' or self.action == 'partial_update':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'list' or self.action == 'destroy' or self.action == 'update':
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
    


class PasswordResetView(GenericAPIView):
    """
    Calls Django Auth PasswordResetForm save method.

    Accepts the following POST parameters: email
    Returns the success/fail message.
    """
    serializer_class = PasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        # Return the success message with OK HTTP status
        return Response(
            {"detail": _("Password reset e-mail has been sent.")},
            status=status.HTTP_200_OK
        )


INTERNAL_RESET_URL_TOKEN = "set-password"
INTERNAL_RESET_SESSION_TOKEN = "_password_reset_token"

class PasswordResetConfirmView(PasswordContextMixin, FormView):
    form_class = SetPasswordForm
    post_reset_login = False
    post_reset_login_backend = None
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'registration/password_reset_confirm.html'
    title = _('Enter new password')
    token_generator = default_token_generator

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        assert 'uidb64' in kwargs and 'token' in kwargs

        self.validlink = False
        self.user = self.get_user(kwargs['uidb64'])

        if self.user is not None:
            token = kwargs['token']

            if token == INTERNAL_RESET_URL_TOKEN:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    # If the token is valid, display the password reset form.
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(token, INTERNAL_RESET_URL_TOKEN)
                    return HttpResponseRedirect(redirect_url)

        # Display the "Password reset unsuccessful" page.
        return self.render_to_response(self.get_context_data())

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist, ValidationError):
            user = None
        return user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
        if self.post_reset_login:
            auth_login(self.request, user, self.post_reset_login_backend)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.validlink:
            context['validlink'] = True
        else:
            context.update({
                'form': None,
                'title': _('Password reset unsuccessful'),
                'validlink': False,
            })
        return context
    


class UpdatePassword(views.APIView):
    """
    An endpoint for changing password.
    """
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]}, 
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)