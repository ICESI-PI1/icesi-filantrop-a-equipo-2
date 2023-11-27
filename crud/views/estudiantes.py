from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def estudiantes(request):
    return render(request, 'estudiantes.html')
