from django.urls import path
from . import views

urlpatterns= [
    path('', views.home, name="home"),
    path('contact/', views.contact, name="contact"),
    path('email-verification/', views.email_verification, name="email-verification"),
    path('thank-you/', views.thankyou_page, name="thank-you"),
    path('message-sent/', views.message_sent, name="message-sent"),
    path('resend/', views.resend, name="resend"),


    path('verify/<uidb64>/<token>', views.verify, name='verify')
]

