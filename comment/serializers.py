from rest_framework import serializers
from .models import Comment, ReplyComment, Bookmark


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='username.username')

    class Meta:
        model = Comment
        fields = ('comment', 'username', 'post')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        action = self.context.get('action')
        if action == 'list':
            representation['replies'] = instance.replies.count()
        elif action == 'retrieve':
            representation['replies'] = ReplyCommentSerializer(
                instance.replies.all(),
                many=True
            ).data

        return representation

    def create(self, validated_data):
        user = self.context.get('request').user
        comment = Comment.objects.create(
            username=user,
            **validated_data
        )
        return comment


class ReplyCommentSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="username.username")

    class Meta:
        model = ReplyComment
        fields = "__all__"

    def create(self, validated_data):
        request = self.context.get('request')
        reply = ReplyComment.objects.create(
            username=request.user,
            **validated_data
        )
        return reply


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["username"] = instance.username.username
        representation["comment"] = instance.comment.comment
        return representation
