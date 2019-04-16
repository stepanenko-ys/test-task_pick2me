from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from .views import UserSignup

urlpatterns = [
    path('signup', UserSignup.as_view(), name='signup'),
    path('login', obtain_jwt_token, name='login'),
]
