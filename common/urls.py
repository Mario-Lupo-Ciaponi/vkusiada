from django.urls import path, include
from common import views


urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
]