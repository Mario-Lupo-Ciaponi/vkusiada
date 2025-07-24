from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, CreateView, DetailView, UpdateView
from django.contrib.auth import get_user_model
from django.contrib import messages

from vkusiada.tasks import _send_mail
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
        """
        Get the context data for the contact page.
        This method adds the contact form and the current page identifier to the context.
        """
        kwargs.update(
            {
                "contact_form": self.get_form_class(),
                "current_page": "contact",
            }
        )

        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        """
        Handle the form submission for the contact page.
        This method sends an email using the provided form data and displays a success message.
        """
        email = form.cleaned_data["email"]
        subject = form.cleaned_data["subject"]
        content = form.cleaned_data["content"]

        _send_mail.delay(
            subject=subject,
            message=content,
            from_email=email,
            recipient_list=[settings.DEFAULT_EMAIL],
        )

        messages.success(self.request, message="Email sent successfully!")

        return super().form_valid(form)


class AccountDetails(DetailView):
    model = UserModel
    context_object_name = "user"
    template_name = "accounts/account-details.html"


class EditProfileView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = "accounts/profile-edit.html"

    def get_success_url(self):
        """
        Get the URL to redirect to after a successful profile edit.
        """
        return reverse(
            "account-details",
            kwargs={
                "pk": self.object.user.pk,
            },
        )

    def test_func(self):
        """
        Check if the user is allowed to edit the profile.
        Only superusers or the user themselves can edit their profile.
        """
        return (
            self.request.user.is_superuser or self.request.user.pk == self.kwargs["pk"]
        )


@login_required
def follow_or_unfollow_user(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Follow or unfollow a user.
    If the user is already following the target user, they will be unfollowed.
    If the user is not following the target user, they will be followed.
    """
    target_user = get_object_or_404(UserModel, pk=pk)

    if request.user == target_user:
        messages.error(request, "Cannot follow yourself!")
        return redirect("account-details", target_user.pk)

    target_profile = Profile.objects.get(user=target_user)

    if target_profile.followers.filter(pk=request.user.pk).exists():
        target_profile.followers.remove(request.user)
        messages.success(request, f"{target_user.username} unfollowed successfully!")
    else:
        target_profile.followers.add(request.user)
        messages.success(request, f"{target_user.username} followed successfully!")
        # Note: There is a signal that sends a notification email when a user is followed.

    return redirect("account-details", target_user.pk)
