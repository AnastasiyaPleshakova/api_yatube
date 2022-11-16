from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.permissions import IsAuthorOrReadOnly
from api.serializers import CommentSerializer, GroupSerializer
from api.serializers import PostSerializer
from posts.models import Group, Post


def get_post_object(self):
    return get_object_or_404(Post, pk=self.kwargs.get('post_id'))


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticated]

    def get_queryset(self):
        return get_post_object(self).comments

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=get_post_object(self))
