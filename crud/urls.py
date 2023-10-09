from django.urls import path

from .views import views, request_info_update, save_student

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signUp),
    path('login/', views.logIn),
    path('postlog/', views.postLog),
    path('logout/', views.singout),
    path('students_info/', save_student.guardar_estudiante, name='estudiante'),
    path('students_info/', save_student.guardar_estudiante, name='guardar_estudiante'),
    path('askInfoUpdate/', request_info_update.ask_info_update)
]
