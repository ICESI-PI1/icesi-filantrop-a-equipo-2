import pandas as pd
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.views import View
from .forms import UploadFileForm  
from crud.models import Beca,Archivo  



class LoadScholarshipData(View):
    
    def get(self, request):
        form = UploadFileForm()
        archivos = Archivo.objects.all()  # Recupera todos los objetos Archivo de la base de datos
        for archivo in archivos:
            print(f'Nombre del archivo: {archivo.nombre}')
            print(f'Fecha: {archivo.fecha}')
            print(f'Peso: {archivo.peso}')
            print(f'URL del archivo: {archivo.archivo.url}')
        return render(request, 'scholarship_data.html', {
            'form': form,
            'archivos': archivos  # Pasa los archivos a la plantilla
        })
    
    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = Archivo(
                nombre=request.FILES['file'].name,
                peso=request.FILES['file'].size,
                archivo=request.FILES['file']
            )
            archivo.save()
            xls = pd.ExcelFile(request.FILES['file'])
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name)
                for index, row in df.iterrows():
                    try:
                        # Busca el objeto Beca o lo crea si no existe
                        beca, created = Beca.objects.get_or_create(
                            id_estudiante=row['id_estudiante'],
                            defaults={
                                'tipo_beca': row['tipo_beca'],
                                'monto': row['monto_asignado'],
                                'duracion': row['duracion']
                            }
                        )

                        # Si el objeto ya existía y fue recuperado, entonces actualiza los campos necesarios
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
        
