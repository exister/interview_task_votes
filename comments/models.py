from django.conf import settings
from django.db import models
from django.utils.text import Truncator

from core.models import TimeStampedModel
from ratings.models import UpDownRating, BaseVote


class Comment(TimeStampedModel, models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    publication = models.ForeignKey('publications.Publication', related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return '{id} - {text}'.format(id=self.pk, text=Truncator(self.title).chars(50))


class CommentRating(UpDownRating):
    ITEM_CLASS = Comment


class CommentVote(BaseVote):
    RATING_CLASS = CommentRating
