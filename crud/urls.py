
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signUp),
    path('login/', views.logIn),
    path('postlog/', views.postLog),
    path('logout/', views.singout),
    path('askInfoUpdate/', views.ask_info_update)
]
