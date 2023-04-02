from django.urls import path
from . import views

urlpatterns= [
    path("administration/", views.administration_site, name="administration-site"),
    path("administration/users", views.users, name="users"),
    path("administration/messages", views.messages, name="messages"),
    path("administration/exceptions", views.exceptions, name="exceptions"),
    path("administration/excercises", views.excercises, name="excercises"),


]
