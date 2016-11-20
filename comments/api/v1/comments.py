from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from ratings.api.v1.ratings import UpDownVoteMixin

from ...models import Comment


class CommentViewSet(
    UpDownVoteMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    """
    API endpoint that allows to vote for comments.

    vote_up:
    Vote +1 for comment.

    vote_down:
    Vote -1 for comment.

    vote_remove:
    Remove current user's vote for comment.

    votes:
    Get total votes for comment.
    """
    queryset = Comment.objects.all()
