from email.mime.text import MIMEText
import smtplib
from django.conf import settings
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import loginValidateSerializer, SignupValidateSerializer

class SignupAPIView(CreateAPIView):
    serializer_class = SignupValidateSerializer

    def create(self, request, *args, **kwargs):
        # Переопределение метода create для отправки кода подтверждения.
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        validated_data['is_active'] = False
        user = User.objects.create_user(username=validated_data['username'], email=validated_data['email'], password=validated_data['password'])

        # Генерация кода подтверждения и отправка на почту
        confirmation_code = "123456"  # Ваш код генерации
        user.confirmation_code = confirmation_code
        user.confirmation_code_created_at = timezone.now()
        user.save()

        send_confirmation_code_email(user, confirmation_code)
        return Response({'message': 'User created', 'user_id': user.id})

class LoginAPIView(APIView):
    def post(self, request, format=None):
        serializer = loginValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'message': 'Successfully authorized', 'key': token.key})
        return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'Unauthorized'})

class ActivateUser(APIView):
    def get(self, request, code, format=None):
        try:
            user = User.objects.get(confirmation_code=code)
        except User.DoesNotExist:
            raise ValidationError("Invalid activation code.")

        code_created_at = user.confirmation_code_created_at
        if timezone.now() - code_created_at < timedelta(minutes=5):
            user.is_active = True
            user.save()
            return Response("User successfully activated.", status=status.HTTP_200_OK)
        else:
            raise ValidationError("Activation code has expired.")

def send_confirmation_code_email(user, confirmation_code):
    smtp_server = settings.EMAIL_HOST
    smtp_port = settings.EMAIL_PORT
    smtp_username = settings.EMAIL_HOST_USER
    smtp_password = settings.EMAIL_HOST_PASSWORD

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)

    subject = 'User Confirmation'
    message = f'Your confirmation code: {confirmation_code}'
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = settings.EMAIL_HOST_USER
    msg['To'] = user.email

    server.sendmail(settings.EMAIL_HOST_USER, [user.email], msg.as_string())
    server.quit()


def login_api_view(request):
    return None