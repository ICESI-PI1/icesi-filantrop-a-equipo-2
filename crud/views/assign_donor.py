from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import pandas as pd
from django.http import HttpResponse
from crud.models import *

@login_required
def assign_donor(request):
    return render(request, 'assign_donor.html')