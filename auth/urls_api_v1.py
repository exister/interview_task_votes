from django.conf.urls import url

from .api.v1.login import LoginAPIView


urlpatterns = [
    url(r'^login/$', LoginAPIView.as_view(), name='login')
]
