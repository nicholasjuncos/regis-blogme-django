from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer

from ..blog.models import Post, Follow, Comment, Like, Reply

User = get_user_model()


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        }
    # Define transaction.atomic to rollback the save operation in case of error
    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.save()
        return user


class UserSerializerForPosts(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'username', 'email', 'first_name', 'last_name', 'bio', 'profile_photo', 'cover_photo', 'full_name', 'display_name', 'url']

        extra_kwargs = {
            'url': {'view_name': 'api:user-detail', 'lookup_field': 'username'}
        }


class PostSerializerForUsers(serializers.ModelSerializer):
    author = UserSerializerForPosts()
    user = UserSerializerForPosts()

    class Meta:
        model = Post
        fields = ['id', 'author', 'user', 'status', 'get_status_display', 'post_date', 'title', 'title_sub_text', 'subtitle1', 'text1', 'subtitle2', 'text2', 'cover_image', 'image1', 'image2', 'image3', 'url']
        extra_kwargs = {
            'url': {'view_name': 'api:post-detail', 'lookup_field': 'id'}
        }


class FollowSerializerForUsers(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'user_follower', 'author_followed', 'created', 'url']
        extra_kwargs = {
            'url': {'view_name': 'api:follow-detail', 'lookup_field': 'id'}
        }
        read_only_fields = ['created']


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


class UserSerializer(serializers.ModelSerializer):
    followers = FollowSerializerForUsers(many=True, required=False)
    authors_following = FollowSerializerForUsers(many=True, required=False)
    likes = LikeSerializer(many=True, required=False)
    comments = CommentSerializer(many=True, required=False)
    replies = ReplySerializer(many=True, required=False)
    last_three_articles = PostSerializerForUsers(many=True, required=False)
    published_posts = PostSerializerForUsers(many=True, required=False)
    email = serializers.EmailField(required=False)
    username = serializers.CharField(max_length=252, required=False)

    class Meta:
        model = User
        fields = ['pk', 'id', 'username', 'email', 'first_name', 'last_name', 'bio', 'profile_photo', 'cover_photo', 'full_name', 'display_name', 'last_three_articles', 'followers', 'authors_following', 'followers_usernames', 'following_usernames', 'published_posts', 'likes', 'comments', 'replies', 'articles_liked', 'comments_liked', 'replies_liked', 'url']

        extra_kwargs = {
            'url': {'view_name': 'api:user-detail', 'lookup_field': 'username'}
        }

        read_only_fields = ['followers', 'authors_following', 'last_three_articles', 'published_posts', 'likes', 'comments', 'replies', 'articles_liked', 'comments_liked', 'replies_liked']
