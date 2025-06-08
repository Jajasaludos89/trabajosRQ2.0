from django.db import models

class Cargo(models.Model):
    id=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=100)
    funciones=models.TextField()
    horario=models.CharField(max_length=500)
    requisitos=models.TextField()
    sueldo=models.DecimalField(max_digits=10,decimal_places=2)

    
    logo=models.FileField(upload_to='cargo', null=True, blank=True)
    archivo=models.FileField(upload_to='archivos', null=True, blank=True)

    def __str__(self):
        fila="{0}: {1} {2} {3}"
        return fila.format(self.id,self.nombre,self.sueldo,self.horario)
    
class Mensaje(models.Model):
    id = models.AutoField(primary_key=True)
    destinatario = models.EmailField()
    asunto = models.TextField(max_length=250)  
    mensaje = models.TextField(max_length=250) 
    archivo = models.FileField(upload_to='archivos_adjuntos/', null=True, blank=True)


    



