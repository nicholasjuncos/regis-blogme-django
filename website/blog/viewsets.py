from django.http import Http404
from django.db.models import Q

from rest_framework import filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from ..common.mixins import GetSerializerClassMixin
from .models import Post, Like, Comment, Reply, Follow
from .permissions import IsAuthorOrReadOnly, UserLikeCommentReplyOwnerOrReadOnly
from .serializers import PostSerializer, PostSerializerReadOnly, LikeSerializer, CommentSerializer, ReplySerializer, \
    FollowSerializer


class PostViewSet(GetSerializerClassMixin, ModelViewSet):
    serializer_class = PostSerializer
    serializer_action_classes = {
        'retrieve': PostSerializerReadOnly,
        'list': PostSerializerReadOnly
    }
    queryset = Post.objects.all()
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['post_date']
    ordering = ['-post_date']
    filterset_fields = {
        'author__username': ['exact'],
        'author': ['exact'],
        'status': ['exact'],
        'post_date': ['gte', 'lte', 'exact', 'gt', 'lt']
    }
    search_fields = ['author', 'title', 'text1', 'text2', ]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self, *args, **kwargs):
        # allow superusers to see all users
        if self.request.user.is_superuser:
            return self.queryset
        # by default only show users themselves, alter this filter to allow users to see others
        return self.queryset.filter(Q(author_id=self.request.user.id) | Q(status='P'))


class LikeViewSet(ModelViewSet):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
    lookup_field = 'id'
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created']
    ordering = ['-created']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, UserLikeCommentReplyOwnerOrReadOnly]


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    lookup_field = 'id'
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created', 'modified']
    ordering = ['-created']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, UserLikeCommentReplyOwnerOrReadOnly]


class ReplyViewSet(ModelViewSet):
    serializer_class = ReplySerializer
    queryset = Reply.objects.all()
    lookup_field = 'id'
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created', 'modified']
    ordering = ['-created']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, UserLikeCommentReplyOwnerOrReadOnly]


class FollowViewSet(ModelViewSet):
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()
    lookup_field = 'id'
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created']
    ordering = ['-created']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, UserLikeCommentReplyOwnerOrReadOnly]
