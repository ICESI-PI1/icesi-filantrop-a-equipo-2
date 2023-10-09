from django.urls import path

from .views import views
from .views import request_info_update
from .views import login

urlpatterns = [
    path('', login.signin, name='signin'),
    path('home/', login.home),
    path('signup/', views.signUp),
    path('postlog/', views.postLog),
    path('students_info/', views.guardar_estudiante, name='estudiante'),
    path('students_confirm/', views.confirmacion, name='confirm'),
    path('students_info/', views.guardar_estudiante, name='guardar_estudiante'),
    path('askInfoUpdate/', request_info_update.ask_info_update)
]
