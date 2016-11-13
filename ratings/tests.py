from rest_framework import status

from auth.tests import UserFactory


class BaseVoteTestCaseMixin:
    VOTE_CLASS = None
    RATING_CLASS = None

    def url(self, *args, **kwargs):
        return NotImplemented

    def create_item(self):
        return NotImplemented


class VoteTestCaseMixin(BaseVoteTestCaseMixin):
    def test_auth(self):
        item = self.create_item()

        request = self.client.post(self.url(item, True))
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_already_voted(self):
        user = UserFactory.create()
        item = self.create_item()

        item.get_rating().vote_up(user)

        self.assertEqual(self.VOTE_CLASS.objects.all().count(), 1)
        self.assertEqual(self.RATING_CLASS.objects.all().count(), 1)

        self.client.force_authenticate(user)
        request = self.client.post(self.url(item, True))
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_vote_up(self):
        user = UserFactory.create()
        item = self.create_item()

        self.assertEqual(self.VOTE_CLASS.objects.all().count(), 0)
        self.assertEqual(self.RATING_CLASS.objects.all().count(), 0)

        self.client.force_authenticate(user)
        request = self.client.post(self.url(item, True))
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

        self.assertEqual(self.VOTE_CLASS.objects.all().count(), 1)
        self.assertEqual(self.RATING_CLASS.objects.all().count(), 1)

        vote = self.VOTE_CLASS.objects.all().first()
        self.assertEqual(vote.user, user)
        self.assertEqual(vote.value, 1)

        rating = self.RATING_CLASS.objects.all().first()
        self.assertEqual(rating.item, item)
        self.assertEqual(rating.total_up_votes, 1)
        self.assertEqual(rating.total_down_votes, 0)
        self.assertEqual(rating.total_votes, 1)

    def test_vote_down(self):
        user = UserFactory.create()
        item = self.create_item()

        self.assertEqual(self.VOTE_CLASS.objects.all().count(), 0)
        self.assertEqual(self.RATING_CLASS.objects.all().count(), 0)

        self.client.force_authenticate(user)
        request = self.client.post(self.url(item, False))
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

        self.assertEqual(self.VOTE_CLASS.objects.all().count(), 1)
        self.assertEqual(self.RATING_CLASS.objects.all().count(), 1)

        vote = self.VOTE_CLASS.objects.all().first()
        self.assertEqual(vote.user, user)
        self.assertEqual(vote.value, -1)

        rating = self.RATING_CLASS.objects.all().first()
        self.assertEqual(rating.item, item)
        self.assertEqual(rating.total_up_votes, 0)
        self.assertEqual(rating.total_down_votes, 1)
        self.assertEqual(rating.total_votes, 1)


class RemoveVoteTestCaseMixin(BaseVoteTestCaseMixin):
    def test_auth(self):
        item = self.create_item()

        request = self.client.delete(self.url(item))
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_voted(self):
        user = UserFactory.create()
        item = self.create_item()

        self.assertEqual(self.VOTE_CLASS.objects.all().count(), 0)
        self.assertEqual(self.RATING_CLASS.objects.all().count(), 0)

        self.client.force_authenticate(user)
        request = self.client.delete(self.url(item))
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove(self):
        user = UserFactory.create()
        item = self.create_item()

        item.get_rating().vote_up(user)

        self.assertEqual(self.VOTE_CLASS.objects.all().count(), 1)
        self.assertEqual(self.RATING_CLASS.objects.all().count(), 1)

        self.client.force_authenticate(user)
        request = self.client.delete(self.url(item))
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(self.VOTE_CLASS.objects.all().count(), 0)
        self.assertEqual(self.RATING_CLASS.objects.all().count(), 1)


class GetVotesTestCaseMixin(BaseVoteTestCaseMixin):
    def test_votes(self):
        item = self.create_item()

        request = self.client.get(self.url(item))
        self.assertEqual(request.status_code, status.HTTP_200_OK)

        self.assertEqual(request.data, {
            'total_up_votes': 0,
            'total_down_votes': 0,
            'total_votes': 0,
        })

