from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import pandas as pd

from crud.models import *


def home(request):
    return render(request, 'home.html')


#@login_required
def upload_CREA_report(request):
    if request.method == 'POST':
        try:
            received_file = request.FILES['report_file']

            file = pd.read_excel(received_file)

            for index, row in file.iterrows():
                fields = {
                    'student_code': row['Código de estudiante'],
                    'name': row['Nombres'],
                    'lastname': row['Apellidos'],
                    'monitor_name': row['Nombre monitoría'],
                    'reason': row['Motivo'],
                    'result': row['Resultado'],
                    'date': row['Fecha'],
                    'hour': row['Hora']
                }

                exists_row = CREAReport.objects.filter(student_code=row['Código de estudiante'],
                                                       monitor_name=row['Nombre monitoría'],
                                                       date=row['Fecha'],
                                                       hour=row['Hora'])
                
                if exists_row:
                    exists_row.update(**fields)

                else:
                    report = CREAReport.objects.create(**fields)
                    report.save()


            result_message = "Carga exitosa"

        except Exception as e:
            result_message = "Error al cargar reporte"
        
        return render(request, 'upload_CREA_report.html', {
            'result_message' : result_message
        })

    return render(request, 'upload_CREA_report.html')