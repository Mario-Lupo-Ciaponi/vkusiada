from django.urls import path, include
from common import views


urlpatterns = [
    path("", views.index_view, name="index"),
    path("about-us/", views.about_us_view, name="about-us")
]