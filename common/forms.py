from django import forms
from common.choices import CategoryChoices


class SearchForm(forms.Form):
    CATEGORY_CHOICES = [("All", "All")] + list(CategoryChoices.choices)

    query = forms.CharField(
        label="",
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Search..."}),
    )
    category = forms.ChoiceField(
        label="",
        required=False,
        choices=CATEGORY_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "search-select",
            }
        ),
    )
    date_added = forms.BooleanField(
        required=False,
        label="Latest",
        initial=True,
    )
