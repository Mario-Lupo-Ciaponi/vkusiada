from django import forms
from .models import Comment


class SearchForm(forms.Form):
    query = forms.CharField(
        label="",
        required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={"placeholder": "Search recipes..."}
        )
    )

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
