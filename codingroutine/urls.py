from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('', include('administration.urls')), 

]

handler404 = 'base.views.page_not_found'