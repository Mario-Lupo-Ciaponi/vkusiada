from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content",]

        labels = {
            "content": "",
        }

        widgets = {
            "content": forms.widgets.TextInput(
                attrs={
                    "placeholder": "Add a comment..."
                }
            )
        }
