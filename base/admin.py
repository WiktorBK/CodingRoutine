from django.contrib import admin
from .models import Newsletter_User, MessageContact, CodingExcercise, ExceptionTracker

# registering models inside admin panel

admin.site.register(Newsletter_User)
admin.site.register(MessageContact)
admin.site.register(CodingExcercise)


