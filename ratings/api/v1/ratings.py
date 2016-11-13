from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.response import Response


class UpDownVoteMixin:
    def _vote(self, request, up=True):
        instance = self.get_object()
        rating = instance.get_rating()

        if not rating.has_voted(request.user):
            if up:
                rating.vote_up(request.user)
            else:
                rating.vote_down(request.user)

            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_403_FORBIDDEN)

    @detail_route(methods=['post'], url_path='vote-up')
    def vote_up(self, request, *args, **kwargs):
        return self._vote(request, up=True)

    @detail_route(methods=['post'], url_path='vote-down')
    def vote_down(self, request, *args, **kwargs):
        return self._vote(request, up=False)

    @detail_route(methods=['delete'], url_path='vote-remove')
    def vote_remove(self, request, *args, **kwargs):
        instance = self.get_object()
        rating = instance.get_rating()

        if rating.has_voted(request.user):
            rating.vote_remove(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_404_NOT_FOUND)

    @detail_route()
    def votes(self, request, *args, **kwargs):
        instance = self.get_object()
        rating = instance.get_rating()

        return Response({
            'total_up_votes': rating.total_up_votes,
            'total_down_votes': rating.total_down_votes,
            'total_votes': rating.total_votes,
        })
