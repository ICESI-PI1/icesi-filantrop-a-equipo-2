<<<<<<< HEAD
import os
import zipfile
=======
from crud.models import Student, Document
>>>>>>> 55b9596eeafe88b5af7f3458e27a03de23387622
from django.shortcuts import render
import os

<<<<<<< HEAD

def procesar_zip(request):
    if request.method == 'POST' and request.FILES.get('archivo_zip'):
        archivo_zip = request.FILES['archivo_zip']
        if archivo_zip.name.endswith('.zip'):
            # Extraer archivos del ZIP
            with zipfile.ZipFile(archivo_zip, 'r') as zip_ref:
                # Carpeta temporal para extraer los archivos
                extract_folder = '/path/to/temp/folder'  # Ruta a tu carpeta temporal
                zip_ref.extractall(extract_folder)
=======
def uploadFile(request):
    result_message = None
>>>>>>> 55b9596eeafe88b5af7f3458e27a03de23387622

    if request.method == "POST":
        # Fetching the form data
        #fileTitle = request.POST["fileTitle"]
        uploadedFile = request.FILES.get("uploadedFile")

        if not uploadedFile:
            result_message = "No se proporcionó ningún archivo."
            return render(request, "upload_academic_report.html", context={"result_message": result_message})

        # Extract student code from file name
        codigo_estudiante = os.path.splitext(uploadedFile.name)[0]

        # Look up student in the database
        try:
            student = Student.objects.get(student_code=codigo_estudiante)
        except Student.DoesNotExist:
            # Handle the case where the student does not exist
            result_message = f"Estudiante con código {codigo_estudiante} no encontrado en la base de datos."
            return render(request, "upload_academic_report.html", context={"result_message": result_message})

        # Saving the information in the database
        try:
            document = Document(uploadedFile=uploadedFile, codigo_estudiante=student)
            document.save()
            result_message = "Archivo cargado exitosamente."
        except Exception as e:
            result_message = f"Error al cargar el archivo: {e}"
    
    documents = Document.objects.all()

    return render(request, "upload_academic_report.html", context={"files": documents, "result_message": result_message})
