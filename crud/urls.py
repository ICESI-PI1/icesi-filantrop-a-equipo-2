from django.urls import path

from .views import login, save_student, request_info_update, upload_scholarship_data, upload_non_academic_report, estudiantes, upload_CREA_report, upload_academic_report, send_report_to_donor, api,donors, reportes, home


urlpatterns = [
    path('', login.signin, name='signin'),
    path('home/', home.contar_registers),
    path('students_info/', save_student.save_student, name='guardar_estudiante'),
    path('askInfoUpdate/', request_info_update.ask_info_update, name='ask_info_update'),
    path('estudiantes/', estudiantes.estudiantes),
    path('info-financiera/', upload_scholarship_data.LoadScholarshipData.as_view(), name='info-financiera'),
    path('uploadNonAcademicReport/', upload_non_academic_report.upload_non_academic_report),
    path('uploadCREAReport/', upload_CREA_report.upload_CREA_report, name='upload_crea_report'),
    path('uploadAcademicReport/', upload_academic_report.uploadFile,  name='uploadFile'),
    path('sendReportToDonor/', send_report_to_donor.send_report_to_donor, name='send_report_to_donor'),
    path('api/getStudents/', api.get_students, name='get-students'),
    path('api/getDonors/', api.get_donors, name='get-donors'),
    path('reportes/', reportes.reportes),
    path('create_donor/', donors.save_donor, name='save_donor'),
    path('sendReport/', send_report_to_donor.send_report, name='send_report'),
    path('list-Students/',home.listar_alumnos),
    path('list-Donors/', home.listar_donantes)
]

