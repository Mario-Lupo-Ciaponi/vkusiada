from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, CreateView, DetailView, UpdateView
from django.contrib.auth import get_user_model, login

from .forms import RegistrationForm, ContactForm, ProfileEditForm
from .models import Profile


UserModel = get_user_model()


class RegisterUserView(CreateView):
    form_class = RegistrationForm
    template_name = "registration/register-form.html"
    success_url = reverse_lazy("login")

    # Note: There is a signal that creates a profile.


class ContactView(FormView):
    form_class = ContactForm
    
    success_url = reverse_lazy("index")
    template_name = "accounts/contact.html"
    
    def get_context_data(self, **kwargs):
        kwargs.update({
            "contact_form": self.get_form_class(),
            "current_page": "contact",
        })
        
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        print("Email sent!")
        super().form_valid(form)


class AccountDetails(DetailView):
    model = UserModel
    context_object_name = "user"
    template_name = "accounts/account-details.html"


class EditProfileView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = "accounts/profile-edit.html"

    def get_success_url(self):
        return reverse(
            "account-details",
            kwargs={
                "pk": self.object.user.pk,
            }
        )

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.pk == self.kwargs["pk"]
