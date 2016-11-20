from auth.urls_api_v1 import urlpatterns as urlpatterns_auth
from publications.urls_api_v1 import urlpatterns as urlpatterns_publications
from comments.urls_api_v1 import urlpatterns as urlpatterns_comments


app_name = 'v1'

urlpatterns = []
urlpatterns += urlpatterns_auth
urlpatterns += urlpatterns_publications
urlpatterns += urlpatterns_comments
