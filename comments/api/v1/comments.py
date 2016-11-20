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
    queryset = Comment.objects.all()
