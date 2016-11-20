from rest_framework.routers import DefaultRouter

from .api.v1.comments import CommentViewSet


router = DefaultRouter()
router.register(r'comments', CommentViewSet)

urlpatterns = router.urls
