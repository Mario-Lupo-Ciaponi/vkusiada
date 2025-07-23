from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from accounts import views

urlpatterns = [
    path("register/", views.RegisterUserView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path(
        "<int:pk>/",
        include(
            [
                path(
                    "",
                    views.AccountDetails.as_view(),
                    name="account-details"
                ),
                path(
                    "edit-profile/",
                    views.EditProfileView.as_view(),
                    name="edit-profile",
                ),
            ]
        ),
    ),
]
