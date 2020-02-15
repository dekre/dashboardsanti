from django.shortcuts import render
from django.template import loader
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.decorators.clickjacking import xframe_options_exempt
import django
import json
import os
from santidash.settings import BASE_DIR



class Index(LoginRequiredMixin,TemplateView):
    template_name = "index.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        return context