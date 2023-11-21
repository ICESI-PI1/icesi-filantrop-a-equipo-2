from django.shortcuts import render
from crud.models import Student, Donor, Alerta
from django.http import HttpRequest

def delete_alert(request, id_alert):
    alerta = Alerta.objects.get(pk=id_alert)
    alerta.delete()
    alertas = Alerta.objects.all()
    return render(request, "listaAlertas.html", {"alertas": alertas, "mensaje": 'OK'})