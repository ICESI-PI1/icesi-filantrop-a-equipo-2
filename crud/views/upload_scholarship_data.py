import pandas as pd
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.views import View
from .forms import UploadFileForm  
from crud.models import Beca,Archivo  
from datetime import datetime
import time



class LoadScholarshipData(View):
    
    def get(self, request):
        form = UploadFileForm()
        archivos = Archivo.objects.all()  
        for archivo in archivos:
            print(f'Nombre del archivo: {archivo.nombre}')
            print(f'Fecha: {archivo.fecha}')
        return render(request, 'scholarship_data.html', {
            'form': form,
            'archivos': archivos  
        })
    
    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = Archivo(
                nombre=request.FILES['file'].name,
                fecha=datetime.now()
                )
            archivo.save()
            xls = pd.ExcelFile(request.FILES['file'])
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name)
                for index, row in df.iterrows():
                    try:
                        beca, created = Beca.objects.get_or_create(
                            id_estudiante=row['id_estudiante'],
                            defaults={
                                'tipo_beca': row['tipo_beca'],
                                'monto': row['monto_asignado'],
                                'duracion': row['duracion']
                            }
                        )
                        if not created:
                            beca.tipo_beca = row['tipo_beca']
                            beca.monto = row['monto_asignado']
                            beca.duracion = row['duracion']
                            beca.save()

                    except Exception as e:
                        messages.error(request, f'Hubo un error al cargar el archivo: {str(e)}')
                messages.success(request, 'Se cargaron las becas correctamente')
        else:
            messages.error(request, 'El formulario no es válido')
        return render(request, 'scholarship_data.html', {
            'form': form})
        
