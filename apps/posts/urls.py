from django.urls import path
from posts import views


urlpatterns = [
    path('', views.PostsListCreateView.as_view(), name='posts'),
    path('like/<int:pk>', views.PostLikeView.as_view(), name='like'),
]
