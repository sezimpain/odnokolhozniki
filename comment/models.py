from django.db import models


class Created(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Comment(Created):
    comment = models.TextField()
    username = models.ForeignKey(
        'account.User',
        related_name='comments',
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        'post.Post',
        related_name='comments',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.comment

    class Meta:
        ordering = ('created',)


class ReplyComment(Created):
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='replies',
        null=False,
        blank=False
    )
    username = models.ForeignKey(
        'account.User',
        on_delete=models.CASCADE,
        related_name='replies'
    )
    reply = models.CharField(
        max_length=255
    )

    class Meta:
        ordering = ('created',)


class Bookmark(models.Model):
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="bookmarks"
    )
    username = models.ForeignKey(
        'account.User',
        on_delete=models.CASCADE,
        related_name="bookmarks"
    )
    favorite = models.BooleanField(
        default=False
    )
