from django.conf.urls import url, include

app_name = 'api'

urlpatterns = [
    url(r'v1/', include('ratings_example.urls_api_v1')),
]
