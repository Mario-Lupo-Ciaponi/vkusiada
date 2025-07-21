from django.http import HttpResponse
from django.shortcuts import redirect

from common.forms import SearchForm


class SlugUrlKwargMixin:
    slug_url_kwarg = "recipe_slug"


class FormValidMixin:
    def form_valid(self, form) -> HttpResponse:
        context = self.get_context_data()
        formset = context["formset"]

        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()  # handles deletions!
            return redirect(self.get_success_url())

        return self.render_to_response(self.get_context_data(form=form))


class TestFuncMixin:
    def test_func(self) -> bool:
        obj = self.get_object()

        return (
                self.request.user.pk == obj.author.pk or
                self.request.user.is_superuser or
                self.request.user.groups.filter(name="Recipe Editor").exists())


class TestFuncCommentMixin:
    def test_func(self) -> bool:
        return (
                self.request.user.pk == self.get_object().author.pk or
                self.request.user.is_superuser)
