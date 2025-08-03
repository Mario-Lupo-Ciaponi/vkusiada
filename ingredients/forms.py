from django import forms

from ingredients.models import Ingredient


class IngredientBaseForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ["name"]

        labels = {
            "name": "",
        }

        error_messages = {
            "name": {"unique": "Oh, no! Seems like this ingredient is already added!"}
        }

        widgets = {
            "name": forms.widgets.TextInput(
                attrs={"placeholder": "Type Ingredient's name"}
            )
        }


class IngredientAddForm(IngredientBaseForm): ...
