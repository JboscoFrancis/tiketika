from django.urls import path,include
from . import views

urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('login/', views.agent_login, name='login'),
    path('logout/', views.agent_logout, name='logout'),
]