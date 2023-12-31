
from django.contrib.auth.decorators import login_required

from crud.models import *
from django.http import JsonResponse


@login_required
def get_students(request):
    students = Student.objects.all().values(
        'id', 'student_code', 'name').order_by('student_code')
    return JsonResponse(list(students), safe=False)


@login_required
def get_donors(request):
    donors = Donor.objects.all().values(
        'id', 'nit', 'name', 'lastname', 'email').order_by('nit')
    return JsonResponse(list(donors), safe=False)
