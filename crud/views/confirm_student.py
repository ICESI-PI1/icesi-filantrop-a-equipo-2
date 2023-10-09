from django.shortcuts import render


def confirmacion(request):
    return render(request, 'students_confirm.html')
