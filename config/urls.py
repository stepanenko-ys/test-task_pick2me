from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import Group, User

admin.site.unregister(Group)
admin.site.unregister(User)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('rest_framework.urls')),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/posts/', include('posts.urls')),
]
