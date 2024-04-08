from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import redirect


class Landing(TemplateView):
    template_name = "landingPage.html"
