from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import FormView

from accounts.forms import ContactForm

class ContactView(FormView):
    form_class = ContactForm
    
    success_url = reverse_lazy("index")
    template_name = "accounts/contact.html"
    
    def get_context_data(self, **kwargs):
        kwargs.update({
            "contact_form": self.get_form_class(),
            "current_page": "contact",
        })
        
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        print("Email sent!")
        super().form_valid(form)
