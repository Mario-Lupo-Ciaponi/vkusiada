from django import forms
from django.core.validators import MinLengthValidator
from .mixins import MakeAllFieldsRequiredMixin, MakeAllFieldNotHavingLabelsMixin


class ContactForm(MakeAllFieldsRequiredMixin, MakeAllFieldNotHavingLabelsMixin, forms.Form):
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
        )
    )

    content = forms.CharField(
        max_length=500,
        validators=[
            MinLengthValidator(10),
        ],
        widget=forms.Textarea(
            attrs={
                "cols": 50,
                "placeholder": "Content"
            }
        ),
    )
