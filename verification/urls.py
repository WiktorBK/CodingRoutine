from django.urls import path
from . import views

urlpatterns= [
    path('email-verification/', views.email_verification, name="email-verification"),

    path('resend/<email>', views.resend, name="resend"),
    path('unsubscribe/<uidb64>/<token>', views.unsubscribe, name='unsubscribe'),
    path('verify/<uidb64>/<token>', views.verify, name='verify')
]