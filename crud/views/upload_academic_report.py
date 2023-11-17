import os
import zipfile
from django.shortcuts import render
from django.contrib import messages
from crud.models import Student


def procesar_zip(request):
    if request.method == 'POST' and request.FILES.get('archivo_zip'):
        archivo_zip = request.FILES['archivo_zip']
        if archivo_zip.name.endswith('.zip'):
            # Extraer archivos del ZIP
            with zipfile.ZipFile(archivo_zip, 'r') as zip_ref:
                # Carpeta temporal para extraer los archivos
                extract_folder = '/path/to/temp/folder'  # Ruta a tu carpeta temporal
                zip_ref.extractall(extract_folder)

            # Leer archivos PDF en la carpeta temporal
            for root, dirs, files in os.walk(extract_folder):
                for filename in files:
                    if filename.endswith('.pdf'):
                        # Procesar el nombre del archivo PDF para obtener el código del estudiante
                        # Suponiendo que el nombre del archivo contiene el código
                        codigo_estudiante = filename.split('.pdf')[0]

                        # Buscar el estudiante en la base de datos
                        try:
                            estudiante = Student.objects.get(codigo=codigo_estudiante)
                            # Aquí puedes relacionar el PDF con el estudiante
                            # Puedes guardar el nombre del archivo o realizar otras operaciones
                        except Student.DoesNotExist:
                            messages.warning(request, f'El estudiante con código {codigo_estudiante} no existe.')

            # Limpia la carpeta temporal después de procesar los archivos
            for root, dirs, files in os.walk(extract_folder):
                for filename in files:
                    os.remove(os.path.join(root, filename))
            os.rmdir(extract_folder)

            messages.success(request, 'Archivos PDF procesados correctamente.')
        else:
            messages.error(request, 'El archivo no es un archivo ZIP.')

    return render(request, 'upload_academic_report.html')
