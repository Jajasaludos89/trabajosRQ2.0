from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio),
    path('nuevoCargo/', views.nuevoCargo),
    path('guardarCargo/', views.guardarCargo),
    path('eliminarCargo/<int:id>/', views.eliminarCargo),
    path('editarCargo/<int:id>/', views.editarCargo),
    path('procesarEdicionCargo/', views.procesarEdicionCargo),
    
    path('listarMensajes/', views.listarMensajes),
    path('nuevoMensaje/', views.nuevoMensaje),
    path('guardarMensaje/', views.guardarMensaje),
    path('eliminarMensaje/<int:id>/', views.eliminarMensaje),
    path('editarMensaje/<int:id>/', views.editarMensaje),
    path('procesarEdicionMensaje/', views.procesarEdicionMensaje),
    path('enviarMensaje/<int:id>/', views.enviarMensaje),

]
