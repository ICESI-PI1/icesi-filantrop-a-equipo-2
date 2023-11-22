from crud.models import Student, Document
from django.shortcuts import render
import os


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
            document = Document(uploadedFile=uploadedFile,
                                codigo_estudiante=student)
            document.save()
            result_message = "Archivo cargado exitosamente."
        except Exception as e:
            result_message = f"Error al cargar el archivo: {e}"

    documents = Document.objects.all()

    return render(request, "upload_academic_report.html", context={"files": documents, "result_message": result_message})
