from django.shortcuts import redirect


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
