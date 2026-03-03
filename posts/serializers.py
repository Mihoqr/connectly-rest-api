from rest_framework import serializers
from django.contrib.auth.models import User 
from .models import Post, Comment

class UserSerializer(serializers.ModelSerializer):
    # Idagdag ang password field at gawin itong write_only para hindi makita sa GET requests
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password'] 

    def create(self, validated_data):
        # GAMITIN ITO: create_user() ang nagha-hash ng password gamit ang Argon2/PBKDF2
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class PostSerializer(serializers.ModelSerializer):
    comments = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'post_type', 'metadata', 'author', 'created_at', 'comments']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'post', 'created_at']

    def validate_post(self, value):
        # Note: value dito ay object na, kaya value.id ang ginagamit
        if not Post.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Post not found.")
        return value

    def validate_author(self, value):
        if not User.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Author not found.")
        return value