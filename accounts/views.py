from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import loginValidateSerializer, SignupValidateSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
import smtplib
from email.mime.text import MIMEText
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

@api_view(['POST'])
def login_api_view(request):
    serializer = loginValidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = authenticate(**serializer.validated_data)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'message': 'Успешная авторизация', 'key': token.key})
    return Response(data={'message': 'Не авторизован'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def signup_api_view(request):
    serializer = SignupValidateSerializer(data=request.data)
    if serializer.is_valid():
        validated_data = serializer.validated_data
        validated_data['is_active'] = False
        user = User.objects.create_user(**validated_data)
        return Response(data={'message': 'Пользователь создан', 'user_id': user.id})
    else:
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def activate_user_with_confirmation_code(request, code):
    try:
        user = User.objects.get(confirmation_code=code)
    except User.DoesNotExist:
        return Response("Неверный код активации.", status=status.HTTP_400_BAD_REQUEST)

    code_created_at = user.confirmation_code_created_at
    if timezone.now() - code_created_at < timedelta(minutes=5):
        user.is_active = True
        user.save()
        return Response("Пользователь успешно активирован.", status=status.HTTP_200_OK)
    else:
        return Response("Срок действия кода истек.", status=status.HTTP_400_BAD_REQUEST)

def send_confirmation_code_email(user, confirmation_code):
    smtp_server = settings.EMAIL_HOST
    smtp_port = settings.EMAIL_PORT
    smtp_username = settings.EMAIL_HOST_USER
    smtp_password = settings.EMAIL_HOST_PASSWORD

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)

    subject = 'Подтверждение пользователя'
    message = f'Ваш код подтверждения: {confirmation_code}'
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = settings.EMAIL_HOST_USER
    msg['To'] = user.email

    server.sendmail(settings.EMAIL_HOST_USER, [user.email], msg.as_string())
    server.quit()
