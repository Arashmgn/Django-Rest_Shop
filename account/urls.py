from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import *


urlpatterns = [
    path('register/', Register.as_view()),
    path('auth-token/', obtain_auth_token),
    path('revoke-token/', RevokeToken.as_view()),
    path('verify-email/<slug:token>/', verify_email),
    path('request-email-verification/',request_email_verification),
]
 
 
 
 
 
 
 
 
  