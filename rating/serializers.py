from django.db.models import Avg
from rest_framework import serializers


from rating.models import Rating



class RatingSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='username.username')

    class Meta:
        model = Rating
        fields = ('rating', 'username', 'profile')

    def create(self, validated_data):
        user = self.context.get('request').user
        rating = Rating.objects.create(
            username=user,
            **validated_data
        )
        return rating

    def get_user(self, user_rating):
        user = user_rating.profile.username
        return user



    def validate_rating(self, rating):
        if rating not in range(1, 6):
            raise serializers.ValidationError(
                "Рейтинг должен быть от 1 до 5"
            )
        return rating




