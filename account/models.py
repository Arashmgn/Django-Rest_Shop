from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):    
    username = None
    email = models.EmailField(_('Email Address'), max_length=50, unique=True)
    is_email_verified = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False, verbose_name='staff')
    zip_code = models.IntegerField(blank=True, null=True)
    address  = models.TextField(blank=True, null=True)
    phone_no = models.IntegerField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
 


class EmailOTP(models.Model):
    
    user                    = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,)
    email_verification_code = models.CharField(max_length=255)


    def is_expired(self,):
        return self.expiration_date < timezone.now()
    
    def return_date_time():
        now = timezone.now()
        return now + timezone.timedelta(days=7)
    
    expiration_date         = models.DateTimeField(default=return_date_time)

    