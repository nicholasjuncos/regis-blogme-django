from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission. Superusers or post authors are the only users who can make edits.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True
        if request.method in permissions.SAFE_METHODS:
            if view.action in ['create', 'post', 'delete']:
                return False
            return obj.status == 'P'

        # Write permissions are only allowed to the owner of the snippet.
        return obj.author == request.user


class UserLikeCommentReplyOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission. Superusers or post authors are the only users who can make edits.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True
        if request.method in permissions.SAFE_METHODS:
            if view.action in ['create', 'post', 'delete']:
                return False
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user


class UserFollowOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission. Superusers or post authors are the only users who can make edits.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True
        if request.method in permissions.SAFE_METHODS:
            if view.action in ['create', 'post', 'delete']:
                return False
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.user_follower == request.user
