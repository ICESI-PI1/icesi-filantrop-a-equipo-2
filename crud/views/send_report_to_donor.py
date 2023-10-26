from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from crud.models import *
from django.http import JsonResponse


def home(request):
    return render(request, 'home.html')


@login_required
def send_report_to_donor(request):
    students = Student.objects.all().order_by('student_code')[:3]
    donors = Donor.objects.all().order_by('name')[:3]


    return render(request, 'send_report_to_donor.html', {
        "students" : students,
        "donors" : donors
    })