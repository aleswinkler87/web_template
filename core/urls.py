from django.urls import path
from .views import (home, about, privacy_policy)

urlpatterns = [
    path("", home, name="home"),
    path("about/", about, name="about"),
    path("privacy-policy/", privacy_policy, name="privacy_policy"),
]