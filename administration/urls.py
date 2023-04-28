from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns= [
    path("administration/", views.administration_site, name="administration-site"),
    path("administration/users", views.users, name="users"),
    path("administration/messages", views.contact_messages, name="messages"),
    path("administration/exceptions", views.exceptions, name="exceptions"),
    path("administration/exercises", views.exercises, name="exercises"),
    path("administration/admins", views.admins, name="admins"),
    path("administration/exercises/add", views.add_exercise, name="add-exercise"),
    path("administration/exercise/<eid>/edit", views.edit_exercise, name="edit-exercise"),
    path("administration/messages/<mid>", views.message, name="message"),
    path("administration/exception/<eid>", views.exception, name="exception"),
    path("administration/messages/<mid>/delete", views.delete_message, name="delete-message"),

    path('administration/logout/', views.logoutUser, name='logout'),
    path('administration/login/', views.loginPage, name='login'),

]
