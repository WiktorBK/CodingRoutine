from django.urls import path
from . import views

urlpatterns= [
    path("administration/", views.administration_site, name="administration-site")
]
