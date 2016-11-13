from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .api.v1.publications import NewsViewSet, ArticleViewSet


router = DefaultRouter()
router.register(r'news', NewsViewSet)
router.register(r'articles', ArticleViewSet)

urlpatterns = router.urls
