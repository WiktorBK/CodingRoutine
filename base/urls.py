from django.urls import path
from . import views

urlpatterns= [
    path('', views.home, name="home"),
    path('contact/', views.contact, name="contact"),
    path('thank-you/', views.thankyou_page, name="thank-you"),
    path('message-sent/', views.message_sent, name="message-sent"),
    path('how-to-unsubscribe/', views.unsubscribe_how_to, name="unsubscribe-how-to"),
]
