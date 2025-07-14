from django.shortcuts import redirect

from common.forms import SearchForm


class SlugUrlKwargMixin:
    slug_url_kwarg = "recipe_slug"


class FormValidMixin:
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]

        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()  # handles deletions!
            return redirect(self.get_success_url())

        return self.render_to_response(self.get_context_data(form=form))


class RecipeListViewMixin:
    context_object_name = "recipes"
    query_param = "query"
    paginate_by = 9
    form_class = SearchForm


class TestFuncMixin:
    def test_func(self):
        obj = self.get_object()

        return (
                self.request.user.pk == obj.author.pk or
                self.request.user.is_superuser or
                self.request.user.groups.filter(name="Recipe Editor").exists())


class TestFuncCommentMixin:
    def test_func(self):
        return (
                self.request.user.pk == self.get_object().author.pk or
                self.request.user.is_superuser)
