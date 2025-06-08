from django.shortcuts import render,redirect, get_object_or_404 # type: ignore
#importando el modelo cargo
from .models import Cargo, Mensaje
from django.contrib import messages # type: ignore
import os
from django.conf import settings
import mimetypes
from django.core.mail import EmailMessage


# Create your views here.
#Funcion para renderizar el listado de cargos
def inicio(request):
    listadoCargos=Cargo.objects.all()
    return render(request,"inicio.html",{'cargos':listadoCargos})
#Renderizando el formulario de nuevo cargo
def nuevoCargo(request):
    return render(request,"nuevoCargo.html")
#ALmacenando los datos de cargo en la Bdd
def guardarCargo(request):
    nombre=request.POST["nombre"]    
    funciones=request.POST["funciones"]    
    horario=request.POST["horario"]    
    requisitos=request.POST["requisitos"]    
    sueldo=request.POST["sueldo"]  

    #subiendo archivo
    logoSubido=request.FILES.get("logo")
    archivo=request.FILES.get("archivo")

    nuevoCargo=Cargo.objects.create(nombre=nombre,funciones=funciones,
        horario=horario,requisitos=requisitos,sueldo=sueldo, logo=logoSubido,archivo=archivo)
    
    #Mensaje de confirmacion
    messages.success(request,"Cargo GUARDADO exitosamente")
    return redirect('/')
#Eliminando cargo por ID
def eliminarCargo(request,id):
    cargoEliminar=Cargo.objects.get(id=id)
    if cargoEliminar.logo and os.path.isfile(cargoEliminar.logo.path):
            os.remove(cargoEliminar.logo.path)
    if cargoEliminar.archivo and os.path.isfile(cargoEliminar.archivo.path):
            os.remove(cargoEliminar.archivo.path)
    cargoEliminar.delete()

    messages.success(request,"Cargo ELIMINADO exitosamente")
    return redirect('/')

#Mostrando el formulario de edicion
def editarCargo(request,id):
    cargoEditar=Cargo.objects.get(id=id)
    return render(request, "editarCargo.html", {'cargoEditar': cargoEditar})

def procesarEdicionCargo(request):
    id = request.POST["id"]  
    nombre = request.POST["nombre"]    
    funciones = request.POST["funciones"]    
    horario = request.POST["horario"]    
    requisitos = request.POST["requisitos"]    
    sueldo = request.POST["sueldo"].replace(',','.')
    logo = request.FILES.get("logo")
    archivo = request.FILES.get("archivo")
    
    cargo = Cargo.objects.get(id=id)
    cargo.nombre = nombre
    cargo.funciones = funciones
    cargo.horario = horario
    cargo.requisitos = requisitos
    cargo.sueldo = sueldo
    if logo:
        if cargo.logo and os.path.isfile(cargo.logo.path):
            os.remove(cargo.logo.path)
        cargo.logo = logo
    if archivo:
        if cargo.archivo and os.path.isfile(cargo.archivo.path):
            os.remove(cargo.archivo.path)
        cargo.archivo = archivo
    
    cargo.save()
    
    # Mensaje de confirmación
    messages.success(request, "Cargo ACTUALIZADO exitosamente")
    return redirect('/')

###MENSAJE###

# Mostrar listado de mensajes
def listarMensajes(request):
    mensajes = Mensaje.objects.all()
    return render(request, "listarMensajes.html", {'mensajes': mensajes})

# Mostrar formulario de nuevo mensaje
def nuevoMensaje(request):
    return render(request, "nuevoMensaje.html")

# Guardar nuevo mensaje
def guardarMensaje(request):
    destinatario = request.POST["destinatario"]
    asunto = request.POST["asunto"]
    mensaje_txt = request.POST["mensaje"]
    archivo = request.FILES.get("archivo")

    Mensaje.objects.create(
        destinatario=destinatario,
        asunto=asunto,
        mensaje=mensaje_txt,
        archivo=archivo
    )

    messages.success(request, "Mensaje GUARDADO exitosamente")
    return redirect('/listarMensajes')

# Eliminar mensaje
def eliminarMensaje(request, id):
    mensaje = Mensaje.objects.get(id=id)
    
    # Eliminar archivo adjunto si existe
    if mensaje.archivo and os.path.isfile(mensaje.archivo.path):
        os.remove(mensaje.archivo.path)
    
    mensaje.delete()
    messages.success(request, "Mensaje ELIMINADO exitosamente")
    return redirect('/listarMensajes')

# Mostrar formulario de edición
def editarMensaje(request, id):
    mensajeEditar = Mensaje.objects.get(id=id)
    return render(request, "editarMensaje.html", {'mensajeEditar': mensajeEditar})

# Procesar edición de mensaje
def procesarEdicionMensaje(request):
    id = request.POST["id"]
    destinatario = request.POST["destinatario"]
    asunto = request.POST["asunto"]
    mensaje_txt = request.POST["mensaje"]
    archivo = request.FILES.get("archivo")

    mensaje = Mensaje.objects.get(id=id)
    mensaje.destinatario = destinatario
    mensaje.asunto = asunto
    mensaje.mensaje = mensaje_txt

    if archivo:
        if mensaje.archivo and os.path.isfile(mensaje.archivo.path):
            os.remove(mensaje.archivo.path)
        mensaje.archivo = archivo

    mensaje.save()
    messages.success(request, "Mensaje ACTUALIZADO exitosamente")
    return redirect('/listarMensajes')


def enviarMensaje(request, id):
    try:
        mensaje = Mensaje.objects.get(id=id)
    except Mensaje.DoesNotExist:
        messages.error(request, "El mensaje no existe")
        return redirect('/listarMensajes')

    email = EmailMessage(
        subject=mensaje.asunto,
        body=mensaje.mensaje,
        from_email=settings.EMAIL_HOST_USER,
        to=[mensaje.destinatario],
    )

    # Activar contenido HTML si se desea (opcional)
    email.content_subtype = "html"

    # Adjuntar archivo si existe
    if mensaje.archivo:
        file_path = mensaje.archivo.path
        if os.path.isfile(file_path):
            file_type, _ = mimetypes.guess_type(file_path)
            with open(file_path, 'rb') as f:
                email.attach(mensaje.archivo.name, f.read(), file_type or 'application/octet-stream')

    try:
        email.send(fail_silently=False)
        messages.success(request, "Mensaje ENVIADO exitosamente")
    except Exception as e:
        messages.error(request, f"No se pudo enviar el mensaje: {e}")

    return redirect('/listarMensajes')



