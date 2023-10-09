from django.urls import path

from .views import views
from .views import request_info_update

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signUp),
    path('login/', views.logIn),
    path('postlog/', views.postLog),
    path('logout/', views.singout),
    path('students_info/', views.guardar_estudiante, name='estudiante'),
    path('students_confirm/', views.confirmacion, name='confirm'),
    path('students_info/', views.guardar_estudiante, name='guardar_estudiante'),
    path('askInfoUpdate/', request_info_update.ask_info_update, name='ask_info_update')
]
