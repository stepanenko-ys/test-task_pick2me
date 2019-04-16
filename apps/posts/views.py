from rest_framework import permissions
from rest_framework import generics
from .models import Post
from . import serializers


class PostsListCreateView(generics.ListCreateAPIView):
    model = Post
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = serializers.CreatePostSerializer
    queryset = Post.objects.all()


class PostLikeView(generics.UpdateAPIView):
    model = Post
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = serializers.UpdatePostSerializer
    queryset = Post.objects.all()
