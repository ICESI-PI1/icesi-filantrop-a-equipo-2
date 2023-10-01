
from django.urls import path
from .views import views
from .views import request_info_update

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signUp),
    path('login/', views.logIn),
    path('postlog/', views.postLog),
    path('logout/', views.singout),
    path('askInfoUpdate/', request_info_update.ask_info_update)
]
