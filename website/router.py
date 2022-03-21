from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from .users.viewsets import UserViewSet
from .blog.viewsets import PostViewSet, LikeViewSet, CommentViewSet, ReplyViewSet, FollowViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register('users', UserViewSet)
router.register('blog/posts', PostViewSet)
router.register('blog/likes', LikeViewSet)
router.register('blog/comments', CommentViewSet)
router.register('blog/replies', ReplyViewSet)
router.register('blog/follows', FollowViewSet)

app_name = 'api'

urlpatterns = router.urls
