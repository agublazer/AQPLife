from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, date, time


class Profile(models.Model):
	user 				= models.OneToOneField(User, on_delete=models.CASCADE)
	tipo_idenficacion	= models.CharField(max_length=30)
	identificacion		= models.IntegerField(default=0)

	def __str__(self):
		return str(self.user.get_username())

class Evento(models.Model):
	nombre				=models.CharField(unique=True,max_length=30)
	tipo_evento			=models.CharField(max_length=20)
	fecha_inicio		=models.DateField(default=date.today)
	fecha_fin			=models.DateField(default=date.today)
	def __str__(self):
		return self.nombre

class CategoriaPersonal(models.Model):
	evento 				=models.ForeignKey(Evento,on_delete=models.CASCADE, null=True)
	evento 				=models.ManyToManyField(Evento)
	nombre_categoria	=models.CharField(max_length=20)
	nivel_categoria		=models.IntegerField(default=1)
	def __str__(self):
		return self.nombre_categoria


class Personal(models.Model):
	evento 				=models.ForeignKey(Evento,on_delete=models.CASCADE)
	profile 			=models.ForeignKey(Profile,on_delete=models.CASCADE)
	categoria_personal	=models.ForeignKey(CategoriaPersonal,on_delete=models.CASCADE)
	def __str__(self):
		return str(self.categoria_personal)+str(" ")+str(self.evento.nombre)


class Ambiente(models.Model):
	nombre				=models.CharField(primary_key=True,max_length=30)
	evento				=models.ForeignKey(Evento,on_delete=models.CASCADE)
	
	ubicacion			=models.CharField(max_length=30)
	capacidad			=models.IntegerField(default=0)
	def __str__(self):
		return self.nombre

class Actividad(models.Model):	
	evento 				=models.ForeignKey(Evento,on_delete=models.CASCADE)
	ambiente  			=models.ForeignKey(Ambiente,blank=True,on_delete=models.CASCADE)
	nombre				=models.CharField(unique=True,max_length=20)
	fecha 				=models.DateField(default=date.today)
	hora_inicio			=models.TimeField(blank=True)
	hora_fin			=models.TimeField(blank=True)
	def __str__(self):
		return self.nombre

class MaterialActividad(models.Model):
	actividad 			=models.ForeignKey(Actividad,on_delete=models.CASCADE)
	nombre 				=models.CharField(unique=True,max_length=20)
	cantidad 			=models.IntegerField(default=0)
	stock				=models.IntegerField(default=0)
	def __str__(self):
		return self.nombre

class MaterialAmbiente(models.Model):
	ambiente 			=models.ForeignKey(Ambiente,on_delete=models.CASCADE)
	nombre 				=models.CharField(unique=True,max_length=20)
	cantidad			=models.IntegerField(default=0)
	stock 				=models.IntegerField(default=0)
	def __str__(self):
		return self.nombre

class Paquete(models.Model):
	evento 				=models.ForeignKey(Evento,on_delete=models.CASCADE)
	nombre 				=models.CharField(unique=True,max_length=30)
	descripcion			=models.CharField(max_length=100)
	costo				=models.FloatField(default=0)
	actividad 			=models.ManyToManyField(Actividad)
	def __str__(self):
		return self.nombre

class Transaccion(models.Model):
	evento 				=models.ForeignKey(Evento,on_delete=models.CASCADE)
	factura				=models.CharField(max_length=30)
	motivo				=models.CharField(max_length=100)
	cantidad			=models.FloatField(default=0)
	tipo_transaccion 	=models.CharField(max_length=15)
	def __str__(self):
		return self.factura


class Inscrito(models.Model):
	profile 			=models.ForeignKey(Profile,on_delete=models.CASCADE)
	evento 				=models.ForeignKey(Evento,on_delete=models.CASCADE)
	paquete				=models.ForeignKey(Paquete,on_delete=models.CASCADE)
	estado_inscripcion 	=models.BooleanField(default=False)
	def __str__(self):
		return self.profile.categoria_usuario

class PaqueteActividad(models.Model):
	id_paquete			=models.ForeignKey(Paquete,on_delete=models.CASCADE)
	id_actividad		=models.ForeignKey(Actividad,on_delete=models.CASCADE)
class TipoAsistencia(models.Model):
	nombre 				=models.CharField(max_length=20)
	def __str__(self):
		return self.nombre

class Expositor(models.Model):
	nombre 				=models.CharField(max_length=20)
	apellido 			=models.CharField(max_length=30)
	actividad 			=models.ManyToManyField(Actividad)


class Asistencia(models.Model):
	inscrito 			=models.ForeignKey(Inscrito,on_delete=models.CASCADE)
	actividad 			=models.ForeignKey(Actividad,on_delete=models.CASCADE)
	fecha  				=models.DateField(default=date.today)
	hora 				=models.TimeField(default=datetime.now().time())
	def __str__(self):
		return self.inscrito



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()