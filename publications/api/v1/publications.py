from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from ratings.api.v1.ratings import UpDownVoteMixin
from ...models import Publication


class PublicationViewSet(
    UpDownVoteMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    pass


class NewsViewSet(PublicationViewSet):
    queryset = Publication.objects.news()


class ArticleViewSet(PublicationViewSet):
    queryset = Publication.objects.articles()
