from django.urls import path, include
from . import api


urlpatterns = [
    path("", api.search, name="search"),
]
