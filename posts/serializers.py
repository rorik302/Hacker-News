from rest_framework import serializers

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    """ Сериализатор для моделей постов """

    class Meta:
        model = Post
        fields = '__all__'
