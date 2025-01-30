from django.urls import path
from . import views

app_name = 'Cajero_Pichincha'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('display_bank_services/', views.display_bank_services, name='display_bank_services'),
    path('register/', views.register, name='register'),
]