from django.db import models


class Rating(models.Model):
    rating = models.PositiveSmallIntegerField()
    username = models.ForeignKey(
        'account.User',
        related_name='rating',
        on_delete=models.CASCADE
    )
    profile = models.ForeignKey(
        'profile_.Profile',
        related_name='rating',
        on_delete=models.CASCADE
    )
