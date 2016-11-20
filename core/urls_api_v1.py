from django.conf.urls import url

from .api.v1.docs import swagger_schema_view

app_name = 'v1'

urlpatterns = [
    url(r'^docs/$', swagger_schema_view)
]
