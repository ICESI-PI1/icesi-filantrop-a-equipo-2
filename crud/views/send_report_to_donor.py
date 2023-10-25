from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import pandas as pd

from crud.models import *


def home(request):
    return render(request, 'home.html')


@login_required
def send_report_to_donor(request):
    return render(request, 'send_report_to_donor.html')