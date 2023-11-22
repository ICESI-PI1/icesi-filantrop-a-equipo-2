from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import pandas as pd
from django.http import HttpResponse
from crud.models import *
import traceback


@login_required
def assign_donor(request):
    if request.method == 'POST':
        try:
            donor_id = request.POST.get('donor-id', '')
            student_id = request.POST.get('student-id', '')

            print('Student code:', student_id)

            donor = Donor.objects.get(id=donor_id)
            student = Student.objects.get(id=student_id)

            student.donor = donor

            student.save()

            result_message = "Asignación realizada exitosamente"

        except Exception as e:
            traceback.print_exc()
            print(f'Error: {e}')

            result_message = "Error en la asignación del donante"

        return render(request, 'assign_donor.html', {
            'result_message': result_message
        })

    return render(request, 'assign_donor.html')