from typing import Dict, Any

from django.contrib.auth import get_user_model

from common.forms import SearchForm


UserModel = get_user_model()


class MakeAllFieldsRequiredMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].required = True


class MakeAllFieldNotHavingLabelsMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].label = ""


class SearchUserMixin:
    model = UserModel
    template_name = "accounts/search-user.html"
    context_object_name = "users"
    paginate_by = 7
    form_class = SearchForm
    query_param = "query"

    def get_context_data(self, *, object_list=None, **kwargs) -> Dict[str, Any]:
        """
        It updates the context with the search form and the query parameter.
        This method is called when rendering the template.
        """
        kwargs.update(
            {
                "search_form": self.form_class(),
                "query": self.request.GET.get(self.query_param, ""),
                "is_profile_search_bar": True,
            }
        )
        return super().get_context_data(object_list=object_list, **kwargs)
