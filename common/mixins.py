from typing import Dict, Any

from django.db import models
from django.utils.text import slugify


from .forms import SearchForm


class SlugMixIn(models.Model):
    slug = models.SlugField(
        max_length=150,
        unique=True,
        blank=True,
    )

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class AddedOnMixIn(models.Model):
    added_on = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        abstract = True


class CategoryFilteringMixin:
    category_param = "category"

    def get_context_data(self, *, object_list=None, **kwargs) -> Dict[str, Any]:
        kwargs.update(
            {
                "category": self.request.GET.get(self.category_param, ""),
                "show_category_field": True,
            }
        )
        return super().get_context_data(object_list=object_list, **kwargs)


class RecipeListViewMixin:
    context_object_name = "recipes"
    query_param = "query"
    category_param = "category"
    paginate_by = 9
    form_class = SearchForm
