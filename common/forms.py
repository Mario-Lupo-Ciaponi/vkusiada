from django import forms
from common.choices import CategoryChoices


class SearchForm(forms.Form):
    query = forms.CharField(
        label="",
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Search..."}),
    )
    category = forms.ChoiceField(
        label="",
        required=False,
        choices=CategoryChoices.choices,
        widget=forms.Select(
            attrs={
                "class": "search-select",
            }
        ),
    )
