from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Post, Group, Follow
from api.querysets import return_queryset

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=return_queryset(Group)
    )
    author = SlugRelatedField(slug_field='username',
                              read_only=True)

    class Meta:
        fields = ('id',
                  'text',
                  'pub_date',
                  'author',
                  'image',
                  'group')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        fields = ('id',
                  'author',
                  'post',
                  'text',
                  'created')
        model = Comment


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id',
                  'title',
                  'slug',
                  'description')


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        queryset=return_queryset(User),
        slug_field='username'
    )

    class Meta:
        model = Follow
        fields = ('id',
                  'user',
                  'following')
        validators = [
            UniqueTogetherValidator(
                queryset=return_queryset(Follow),
                fields=('user', 'following')
            )
        ]

    def validate(self, data):
        if data['following'] == self.context['request'].user:
            raise serializers.ValidationError(
                'Имя не должно совпадать с цветом.')
        return data
