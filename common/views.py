from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView


def index_view(request: HttpRequest) -> HttpResponse:
    return render(request, "common/index.html", context={"current_page": "index"})


def about_us_view(request: HttpRequest) -> HttpResponse:
    return render(request, "common/about-us.html", context={"current_page": "about_us"})