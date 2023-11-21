from django.shortcuts import render


def estudiantes(request):
    return render(request, 'estudiantes.html')
