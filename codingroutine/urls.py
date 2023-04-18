from django.contrib import admin
from django.urls import path, include

from secret_values import admin_key

urlpatterns = [
    path(f'{admin_key}/', admin.site.urls),
    path('', include('base.urls')),
    path('', include('administration.urls')), 

]

handler404 = 'base.views.page_not_found'