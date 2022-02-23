from rest_framework import serializers
import like
from comment.serializers import CommentSerializer
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='username.username')
    is_fan = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('caption', 'location', 'post', 'total_likes', 'is_fan', 'username', 'profile')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        action = self.context.get('action')
        if action == 'list':
            representation['comments'] = instance.comments.count()
        elif action == 'retrieve':
            representation['comments'] = CommentSerializer(
                instance.comments.all(),
                many=True
            ).data
        return representation

    def get_is_fan(self, obj) -> bool:
        username = self.context.get('request').user
        return like.services.is_fan(obj, username)

    def create(self, validated_data):
        request = self.context.get('request')
        post = Post.objects.create(username=request.user, **validated_data)
        return post

