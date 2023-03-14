from django.urls import path
from . import views

urlpatterns= [
    path('', views.home, name="home"),
    path('contact/', views.contact, name="contact"),
    path('email-verification/', views.email_verification, name="email-verification"),
    path('thank-you/', views.thankyou_page, name="thank-you"),

]

