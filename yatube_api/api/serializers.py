from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Group, Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'image', 'group', 'pub_date',)

        validators = [
            UniqueTogetherValidator(
                queryset=Post.objects.all(),
                fields=('author', 'text'),
                message='Повторяющийся пост'
            )
        ]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    # можно ли для поста назначит дефолтное значение?
    # post = serializers.StringRelatedField(read_only=True, default=)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')

        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Comment.objects.all(),
        #         fields=('author', 'text', 'post'),
        #         message='Повторяющийся комментарий'
        #     )
        # ]
