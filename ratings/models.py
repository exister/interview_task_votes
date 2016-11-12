from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models

from core.models import TimeStampedModel
from publications.models import Publication


class AbstractVote(TimeStampedModel, models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    value = models.SmallIntegerField()

    class Meta:
        abstract = True


class BaseRating(TimeStampedModel, models.Model):
    ITEM_CLASS = None

    class Meta:
        abstract = True


class PublicationRating(BaseRating):
    ITEM_CLASS = Publication


def prepare_models(sender, **kwargs):
    if issubclass(sender, BaseRating):
        opts = sender._meta
        item_class = getattr(sender, 'ITEM_CLASS', None)
        if item_class is None:
            raise ImproperlyConfigured('`BaseRating` subclasses must define a `ITEM_CLASS`.')

        models.ForeignKey(item_class).contribute_to_class(sender, 'item')

models.signals.class_prepared.connect(prepare_models)