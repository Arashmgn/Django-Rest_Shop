from django.core.mail import send_mail
from django.conf import settings
from .models import User
from django.utils.crypto import get_random_string
import hashlib
import time



def send_otp_via_email(email,otp):
    subject = "Verify your email"
    message = f"Please verify your email using this link \n\n\n 127.0.0.1:8000/account/verify-email/{otp}"
    email_from = settings.EMAIL_HOST
    send_mail(subject,message, email_from, [email])


def get_unique_code(user):
    message = user.email + str(time.now())
    hash_object = hashlib.sha256(message.encode())
    return hash_object.hexdigest()[:8]