from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(
        label="",
        required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={"placeholder": "Search..."}
        )
    )
