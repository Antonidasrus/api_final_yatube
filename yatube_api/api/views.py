from django.shortcuts import get_object_or_404

from rest_framework import viewsets, filters
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from posts.models import Post, Group, Follow
from api.serializers import (PostSerializer,
                             GroupSerializer,
                             CommentSerializer,
                             FollowSerializer)
from api.permissions import IsAuthorAndAuthenticatedOrReadOnly
from api.querysets import return_queryset


class ListCreateViewSet(ListModelMixin,
                        CreateModelMixin,
                        viewsets.GenericViewSet):
    pass


class PostViewSet(viewsets.ModelViewSet):
    queryset = return_queryset(Post)
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthorAndAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorAndAuthenticatedOrReadOnly,)

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        author = self.request.user
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=author, post=post)


class FollowViewSet(ListCreateViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
