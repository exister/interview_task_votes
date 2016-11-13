import factory

from rest_framework.test import APITestCase

from auth.tests import UserFactory
from ratings.tests import VoteTestCaseMixin, RemoveVoteTestCaseMixin, GetVotesTestCaseMixin

from .models import Publication, PublicationVote, PublicationRating


class PublicationFactory(factory.DjangoModelFactory):
    class Meta:
        model = Publication

    author = factory.SubFactory(UserFactory)


class ArticleFactory(PublicationFactory):
    publication_type = factory.LazyAttribute(lambda n: Publication.TYPE_ARTICLE)


class NewsFactory(PublicationFactory):
    publication_type = factory.LazyAttribute(lambda n: Publication.TYPE_NEWS)


class PublicationVoteTestMixin:
    VOTE_CLASS = PublicationVote
    RATING_CLASS = PublicationRating


class ArticleVoteTestMixin(PublicationVoteTestMixin):
    def create_item(self):
        return ArticleFactory.create()


class NewsVoteTestMixin(PublicationVoteTestMixin):
    def create_item(self):
        return NewsFactory.create()


class ArticleVoteTestCase(ArticleVoteTestMixin, VoteTestCaseMixin, APITestCase):
    def url(self, item, up):
        return '/api/v1/articles/{}/vote-{}/'.format(item.pk, 'up' if up else 'down')


class ArticleRemoveVoteTestCase(ArticleVoteTestMixin, RemoveVoteTestCaseMixin, APITestCase):
    def url(self, item):
        return '/api/v1/articles/{}/vote-remove/'.format(item.pk)


class ArticleGetVotesTestCase(ArticleVoteTestMixin, GetVotesTestCaseMixin, APITestCase):
    def url(self, item):
        return '/api/v1/articles/{}/votes/'.format(item.pk)


class NewsVoteTestCase(NewsVoteTestMixin, VoteTestCaseMixin, APITestCase):
    def url(self, item, up):
        return '/api/v1/news/{}/vote-{}/'.format(item.pk, 'up' if up else 'down')


class NewsRemoveVoteTestCase(NewsVoteTestMixin, RemoveVoteTestCaseMixin, APITestCase):
    def url(self, item):
        return '/api/v1/news/{}/vote-remove/'.format(item.pk)


class NewsGetVotesTestCase(NewsVoteTestMixin, GetVotesTestCaseMixin, APITestCase):
    def url(self, item):
        return '/api/v1/news/{}/votes/'.format(item.pk)
