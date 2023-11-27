from crud.models import Student, Document
from django.shortcuts import render
import os
from django.contrib.auth.decorators import login_required


@login_required
def uploadFile(request):
    result_message = None

    if request.method == "POST":
        # Fetching the form data
        # fileTitle = request.POST["fileTitle"]
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
            try:
                os.remove(f'media/Uploaded Files/{codigo_estudiante}.pdf')

            except Exception as e:
                print(f'Error: {e}')

            data = {
                'uploadedFile': uploadedFile,
                'codigo_estudiante': student
            }
            
            document, created = Document.objects.update_or_create(codigo_estudiante=student,
                                                        defaults=data)
                
            result_message = "Archivo cargado exitosamente."
        
        except Exception as e:
            result_message = f"Error al cargar el archivo: {e}"

    documents = Document.objects.all()

    return render(request, "upload_academic_report.html", context={"files": documents, "result_message": result_message})