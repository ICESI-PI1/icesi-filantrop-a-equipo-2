from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def upload_non_academic_report(request):
    return render(request, "upload_non_academic_report.html")