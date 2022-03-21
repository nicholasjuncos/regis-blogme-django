from rest_framework import serializers

from ..users.serializers import UserSerializer
from .models import Post, Like, Comment, Reply, Follow


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id', 'author', 'user', 'status', 'get_status_display', 'post_date', 'title', 'title_sub_text', 'subtitle1', 'text1', 'subtitle2', 'text2', 'cover_image', 'image1', 'image2', 'image3', 'url']
        extra_kwargs = {
            'url': {'view_name': 'api:post-detail', 'lookup_field': 'id'}
        }


class PostSerializerReadOnly(PostSerializer):
    author = UserSerializer()
    user = UserSerializer()


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ['id', 'article', 'user', 'comment', 'reply', 'created', 'url']
        extra_kwargs = {
            'url': {'view_name': 'api:like-detail', 'lookup_field': 'id'}
        }
        read_only_fields = ['created']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'article', 'user', 'comment', 'created', 'modified', 'url']
        extra_kwargs = {
            'url': {'view_name': 'api:comment-detail', 'lookup_field': 'id'}
        }
        read_only_fields = ['created', 'modified']


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ['id', 'comment', 'user', 'reply', 'created', 'modified', 'url']
        extra_kwargs = {
            'url': {'view_name': 'api:reply-detail', 'lookup_field': 'id'}
        }
        read_only_fields = ['created', 'modified']


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'user_follower', 'author_followed', 'created', 'url']
        extra_kwargs = {
            'url': {'view_name': 'api:follow-detail', 'lookup_field': 'id'}
        }
        read_only_fields = ['created']
