from rest_framework import serializers
from .models import Post


class CreatePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'


class UpdatePostSerializer(serializers.ModelSerializer):
    action = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = Post
        fields = ['action', 'id', 'like', 'dislike']

    def update(self, instance, validated_data):
        action = validated_data.get('action', None)

        if action == 'like':
            instance.add_like()

        elif action == 'dislike':
            instance.add_dislike()

        return instance
