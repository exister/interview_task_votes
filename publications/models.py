from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import Truncator
from django_fsm import FSMField, transition

from core.models import TimeStampedModel


class Publication(TimeStampedModel, models.Model):
    TYPE_NEWS = 'news'
    TYPE_ARTICLE = 'article'
    TYPE_CHOICES = (
        (TYPE_NEWS, 'News'),
        (TYPE_ARTICLE, 'Article'),
    )

    STATUS_DRAFT = 'draft'
    STATUS_PUBLISHED = 'published'
    STATUS_CHOICES = (
        (STATUS_DRAFT, 'Draft'),
        (STATUS_PUBLISHED, 'Published'),
    )

    publication_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    status = FSMField(default=STATUS_DRAFT)

    title = models.CharField(max_length=255)
    text = models.TextField()

    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)

    published_at = models.DateTimeField(null=True, blank=True, editable=False)

    def __str__(self):
        return '{id} - {title}'.format(id=self.pk, title=Truncator(self.title).chars(50))

    @transition(field=status, source=STATUS_DRAFT, target=STATUS_PUBLISHED)
    def publish(self):
        self.published_at = timezone.now()
