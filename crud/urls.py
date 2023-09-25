
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signUp),
    path('login/', views.logIn),
    path('postlog/', views.postLog),
    path('logout/', views.singout),
    path('uploadNonAcademicReport/', views.upload_non_academic_report),
]
