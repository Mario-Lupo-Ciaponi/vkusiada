from django import forms
from django.forms.models import inlineformset_factory

from .models import Recipe, Comment, RecipeIngredient


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


class BaseRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ["slug", "users", "ingredients"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Enter recipe name"}),
            "cuisine": forms.TextInput(attrs={"placeholder": "Cuisine"}),
            "youtube_link": forms.URLInput(attrs={"placeholder": "YouTube link (optional)"}),
            "image_url": forms.URLInput(attrs={"placeholder": "Image URL"}),
            "instructions": forms.Textarea(attrs={"placeholder": "Instructions"}),
        }

class CreateRecipeForm(BaseRecipeForm):
    ...

RecipeIngredientFormSet = inlineformset_factory(
    Recipe,
    RecipeIngredient,
    fields=["ingredient", "measure"],
    extra=1,
    can_delete=True,  # Needed for deletions
)

