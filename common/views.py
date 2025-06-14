from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"
    extra_context = {
        "current_page": "index",
    }