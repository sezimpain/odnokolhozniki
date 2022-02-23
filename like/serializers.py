from django.contrib.auth import get_user_model
from rest_framework import serializers

from like.models import Like

User = get_user_model()


class FanSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_full_name(self, obj):
        return obj.get_full_name()

    def create(self, validated_data):
        username = self.context.get('request').user
        like = Like.objects.create(
            username=username,
            **validated_data
        )
        return like


