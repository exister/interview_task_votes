import factory

from rest_framework.test import APITestCase

from auth.tests import UserFactory
from ratings.tests import VoteTestCaseMixin, RemoveVoteTestCaseMixin, GetVotesTestCaseMixin
from publications.tests import PublicationFactory

from .models import Comment, CommentVote, CommentRating


class CommentFactory(factory.DjangoModelFactory):
    class Meta:
        model = Comment

    user = factory.SubFactory(UserFactory)
    publication = factory.SubFactory(PublicationFactory)


class CommentVoteTestMixin:
    VOTE_CLASS = CommentVote
    RATING_CLASS = CommentRating

    def create_item(self):
        return CommentFactory.create()


class CommentVoteTestCase(CommentVoteTestMixin, VoteTestCaseMixin, APITestCase):
    def url(self, item, up):
        return '/api/v1/comments/{}/vote-{}/'.format(item.pk, 'up' if up else 'down')


class CommentRemoveVoteTestCase(CommentVoteTestMixin, RemoveVoteTestCaseMixin, APITestCase):
    def url(self, item):
        return '/api/v1/comments/{}/vote-remove/'.format(item.pk)


class CommentGetVotesTestCase(CommentVoteTestMixin, GetVotesTestCaseMixin, APITestCase):
    def url(self, item):
        return '/api/v1/comments/{}/votes/'.format(item.pk)
