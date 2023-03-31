from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test


@user_passes_test(lambda u: u.is_superuser)
def administration_site(request):
    return render(request, 'administration/administration.html')
