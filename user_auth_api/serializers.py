from rest_framework import serializers

from finalapi import settings
from .forms import PasswordResetForm
from user_auth_api.models import User

class ObtainTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'username', 'last_name', 'email', 'phone_number', 'app_source', 'gender', 'country', 'city', 'state', 'password')
        extra_kwargs = {'password': {'write_only': True}}
        

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(
            username = validated_data.get('username'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            email = validated_data.get('email'),
            phone_number=validated_data.get('phone_number'),
            app_source=validated_data.get('app_source'),
            gender = validated_data.get('gender'),
            country=validated_data.get('country'),
            city=validated_data.get('city'),
            state = validated_data.get('state'),
            )
        # user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.app_source = validated_data.get('app_source', instance.app_source) 
        instance.gender = validated_data.get('gender', instance.gender)
        instance.country = validated_data.get('country', instance.country)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)
        instance.is_approved_to_be_in_touch = validated_data.get('is_approved_to_be_in_touch', instance.is_approved_to_be_in_touch)
        instance.save()

        return instance



class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """
    email = serializers.EmailField()

    password_reset_form_class = PasswordResetForm

    def get_email_options(self):
        """Override this method to change default e-mail options"""
        return {}

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        return value

    def save(self):
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
        }

        opts.update(self.get_email_options())
        self.reset_form.save(**opts)

from django.contrib.auth.password_validation import validate_password

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value