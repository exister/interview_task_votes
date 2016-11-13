from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models

from core.models import TimeStampedModel


class BaseVote(TimeStampedModel, models.Model):
    RATING_CLASS = None

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    value = models.SmallIntegerField()

    class Meta:
        abstract = True


class BaseRatingManager(models.Manager):
    def rating_for_item(self, item):
        return self.get_or_create(item=item)[0]


class BaseRating(TimeStampedModel, models.Model):
    ITEM_CLASS = None

    objects = BaseRatingManager()

    class Meta:
        abstract = True

    def has_voted(self, user):
        return self.votes.filter(user=user).exists()

    def vote_remove(self, user):
        return self.votes.filter(user=user).delete()


class UpDownRating(BaseRating):
    total_up_votes = models.IntegerField()
    total_down_votes = models.IntegerField()
    total_votes = models.IntegerField()

    class Meta:
        abstract = True

    def vote_up(self, user):
        self.votes.get_or_create(user=user, defaults={'value': 1})
        # TODO move to periodic celery task
        self.sum_up()

    def vote_down(self, user):
        self.votes.get_or_create(user=user, defaults={'value': -1})
        # TODO move to periodic celery task
        self.sum_up()

    def sum_up(self):
        self.total_up_votes = self.votes.filter(value=1).aggregate(c=models.Count('id'))['c']
        self.total_down_votes = self.votes.filter(value=-1).aggregate(c=models.Count('id'))['c']
        self.total_votes = self.total_up_votes + self.total_down_votes
        self.save(update_fields=['total_up_votes', 'total_down_votes', 'total_votes'])


def prepare_models(sender, **kwargs):
    if issubclass(sender, BaseRating):
        item_class = getattr(sender, 'ITEM_CLASS', None)
        if item_class is None:
            raise ImproperlyConfigured('`BaseRating` subclasses must define a `ITEM_CLASS`.')

        models.OneToOneField(item_class, related_name='rating').contribute_to_class(sender, 'item')

        def get_rating(self):
            return sender.objects.rating_for_item(self)
        item_class.get_rating = get_rating

    elif issubclass(sender, BaseVote):
        rating_class = getattr(sender, 'RATING_CLASS', None)
        if rating_class is None:
            raise ImproperlyConfigured('`BaseVote` subclasses must define a `RATING_CLASS`.')

        models.ForeignKey(rating_class, related_name='votes').contribute_to_class(sender, 'rating')

models.signals.class_prepared.connect(prepare_models, dispatch_uid='prepare_rating_models')
