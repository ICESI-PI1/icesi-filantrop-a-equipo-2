from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import pandas as pd
from django.http import HttpResponse
from crud.models import *


@login_required
def upload_non_academic_report(request):

    if request.method == 'POST':
         
        try:
            received_file = request.FILES['report_file']
            
            file = pd.read_excel(received_file)
            
            for index, row in file.iterrows():
                fields = {
                    'student_code': row['Código de estudiante'],
                    'name': row['Nombres'],
                    'lastname': row['Apellidos'],
                    'activity': row['Actividad'],
                    'activity_hours': row['Cantidad de horas'],
                    'semester': row['Semestre']
                }

                exists_row = NonAcademicActvitiesReport.objects.filter(student_code=row['Código de estudiante'], 
                                                                       name=row['Nombres'],
                                                                       lastname=row['Apellidos'],
                                                                       activity=row['Actividad'],
                                                                       semester=row['Semestre'])

                if exists_row.exists():
                    exists_row.update(**fields)

                else:
                    report = NonAcademicActvitiesReport.objects.create(**fields)
                    report.save()

            result_message = "Carga exitosa"

        except Exception as e:
            result_message = "Error al cargar reporte"

        return render(request, "upload_non_academic_report.html", {
            'result_message': result_message
        })

    return render(request, "upload_non_academic_report.html")
