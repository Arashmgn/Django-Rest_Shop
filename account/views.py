from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import *
from .serializers import *
from .utils import *


class RevokeToken(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        request.auth.delete()
        return Response(status=204)
    
class Register(APIView):

    def post(self, request):
        try:
            data = request.data
            serializer = UserSerializer(data = data)
            if serializer.is_valid():
                user = serializer.save()  

                email_otp = EmailOTP(user=user, email_verification_code=get_unique_code(user),)
                
                send_otp_via_email(user.email, email_otp.email_verification_code)


                return Response({
                    'status':200,
                    'message':'registered succesfully check email',
                    'data':serializer.data,
                })
            
            return Response({
                'status':400,
                'message':'something went wrong',
                'data': serializer.errors
            })
        
        except Exception as e:
            print(e)


@api_view(["GET",])
@permission_classes([IsAuthenticated])
def request_email_verification(request):
    user = request.user
    if user.is_email_verified:
        return Response({'message': 'your email was verified'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        email_otp                         = EmailOTP.objects.get(user=user)
        email_otp.email_verification_code = get_unique_code()
        email_otp.expiration_date         = email_otp.return_date_time()
        email_otp.save()

    except EmailOTP.DoesNotExist:
        email_otp = EmailOTP(user=user, email_verification_code=get_unique_code(user),)
        email_otp.save()
    

    send_otp_via_email(user.email, email_otp.email_verification_code)
    return Response({'message': 'email was sent to your email address'}, status=status.HTTP_202_ACCEPTED)
        
        


@api_view(["POST",])
def verify_email(request,token):
    try:
        email_otp = EmailOTP.objects.get(email_verification_code=token)
        if email_otp.user.is_email_verified:
            return Response({'message': 'your email is already verified'}, status=status.HTTP_400_BAD_REQUEST)
    
        if email_otp.is_expired():
            return Response({'message': 'expired OTP try getting a new OTP'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = email_otp.user
        user.is_email_verified = True
        user.save()

        return Response({'message': 'email verified succesfully'}, status=status.HTTP_202_ACCEPTED)

    except EmailOTP.DoesNotExist:
        return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)


 