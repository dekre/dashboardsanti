from django.urls import path
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
from athletdash.views import Index 

urlpatterns = [    
     path('', Index.as_view(), name='index')
]

