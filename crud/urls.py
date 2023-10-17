from django.urls import path

from .views import login, save_student, request_info_update, upload_scholarship_data, upload_non_academic_report

urlpatterns = [
    path('', login.signin, name='signin'),
    path('home/', login.home),
    path('students_info/', save_student.guardar_estudiante, name='guardar_estudiante'),
    path('askInfoUpdate/', request_info_update.ask_info_update, name='ask_info_update'),
    path('estudiantes/', save_student.guardar_estudiante),
    path('info-financiera/', upload_scholarship_data.LoadScholarshipData.as_view(), name='info-financiera'),
    path('uploadNonAcademicReport/', upload_non_academic_report.upload_non_academic_report)
]

