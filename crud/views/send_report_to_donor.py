from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from crud.models import *
from django.http import JsonResponse


def home(request):
    return render(request, 'home.html')


@login_required
def send_report_to_donor(request):
    if request.method == 'POST':
        try:
            selected_donor_email = request.POST.get('donor-email', '')

            result_message = "Reporte generado y enviado con éxito"
        except Exception as e:

            result_message = "Error en la generación y envío de reporte"
        
        return render(request, 'send_report_to_donor.html', {
            "result_message" : result_message
        })


    return render(request, 'send_report_to_donor.html')