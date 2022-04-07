from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate
from django.conf import settings
from django.middleware import csrf
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from . import serializers

# Create your views here.

def get_tokens_for_user(user) -> dict[str, str]:
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class LoginView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):

        data = request.data
        response = Response()
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)
                csrftoken = csrf.get_token(request)
                response.set_cookie(
                    key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                    value=data["access"],
                    expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                    domain=settings.SIMPLE_JWT['AUTH_COOKIE_DOMAIN'],
                    path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH']
                )
                response.set_cookie(
                    key='csrftoken',
                    value=csrftoken,
                    expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=False,
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                    domain=settings.SIMPLE_JWT['AUTH_COOKIE_DOMAIN'],
                    path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH']
                )
                response.data = {'success': 'Login successfully',
                                 'email': user.email, 'name': user.name}
                return response
            else:
                return Response({'No active': 'This account is not active!'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'Invalid': 'Invalid username or password!'}, status=status.HTTP_404_NOT_FOUND)

class CreateUserViewSet(viewsets.ModelViewSet):

    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    