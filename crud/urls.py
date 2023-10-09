from django.urls import path

from .views import views, request_info_update,login,estudiantes, upload_scholarship_data

urlpatterns = [
    path('', login.signin, name='signin'),
    path('home/', login.home),
    path('students_confirm/', views.confirmacion, name='confirm'),
    path('students_info/', views.guardar_estudiante, name='guardar_estudiante'),
    path('askInfoUpdate/', request_info_update.ask_info_update),
    path('estudiantes/', estudiantes.estudiantes),
    path('info-financiera/',upload_scholarship_data.LoadScholarshipData.as_view(), name='info-financiera')
]
