from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio),
    path('nuevoCargo/', views.nuevoCargo),
    path('guardarCargo/', views.guardarCargo),
    path('eliminarCargo/<int:id>/', views.eliminarCargo),
    path('editarCargo/<int:id>/', views.editarCargo),
    path('procesarEdicionCargo/', views.procesarEdicionCargo),
    

]
