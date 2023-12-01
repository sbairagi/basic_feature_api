from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core import mail


class User(AbstractUser):
    MALE = 'Male'
    FEMALE = 'Female'
    GENDER_IN_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    gender = models.CharField(max_length=6, choices=GENDER_IN_CHOICES, null=True, blank=True)
    country = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=120, null=True, blank=True)
    state = models.CharField(max_length=120, null=True, blank=True)
    app_source = models.CharField(max_length=50, null=True, blank=True)
    is_approved_to_be_in_touch = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['email', 'phone_number', 'gender', 'country', 'city', 'state', 'app_source']

    class Meta:
        verbose_name = "App User"
        verbose_name_plural = "App Users"

@receiver(post_save, sender=User, dispatch_uid="registration_notification")
def notify_new_user_registration(sender, created, instance, **kwargs):
    if created:
        try:
            subject = 'New user registration on app {} {}'.format(instance.first_name, instance.last_name)
            html_message = render_to_string(
                'admin-notifications/new-user-registration-notification.html',
                {
                    'app_source': instance.app_source,
                    'email': instance.email,
                    'first_name': instance.first_name,
                    'last_name': instance.last_name,
                    'phone_number': instance.phone_number
                 }
            )
            plain_message = strip_tags(html_message)
            from_email = '{} <no-reply@appadminpanel.in>'.format(instance.app_source)
            if instance.app_source == "ifl_services":
                to = 'sbairagi825@gmail.com'
            elif instance.app_source == "EquityGlobal" :
                to = 'sbairagi825@gmail.com'
            else:
                to = 'sbairagi825@gmail.com'
            mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
        except:
            pass