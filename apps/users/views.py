from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from .models import CustomUser
from . import serializers


class UserSignup(CreateAPIView):
    model = CustomUser
    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.UserSignupSerializer
