from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import MinLengthValidator

from .models import Profile
from .mixins import MakeAllFieldsRequiredMixin, MakeAllFieldNotHavingLabelsMixin


UserModel = get_user_model()


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = (
            "username",
            "email",
        )


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = [
            "user",
        ]

        widgets = {
            "bio": forms.widgets.Textarea(
                attrs={
                    "placeholder": "Enter bio",
                }
            ),
            "birth_date": forms.widgets.DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "favourite_cuisine": forms.widgets.TextInput(
                attrs={
                    "placeholder": "Enter favourite cuisine",
                }
            ),
        }


class ContactForm(
    MakeAllFieldsRequiredMixin, MakeAllFieldNotHavingLabelsMixin, forms.Form
):
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
            }
        )
    )

    subject = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Subject",
            }
        ),
    )

    content = forms.CharField(
        max_length=500,
        validators=[
            MinLengthValidator(10),
        ],
        widget=forms.Textarea(attrs={"cols": 50, "placeholder": "Content"}),
    )
