from django.urls import path

from accounts import views

urlpatterns = [
    path("contact/", views.ContactView.as_view(), name="contact")
]