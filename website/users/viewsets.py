from django.contrib.auth import get_user_model

from rest_framework import status, filters, permissions
from rest_framework.decorators import action
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['username', 'email', 'first_name', 'last_name', ]
    search_fields = ['username', 'email', 'first_name', 'last_name', ]
    permission_classes = []

    @action(detail=False, methods=['GET'])
    def me(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)
