from django.db import models

# Create your models here.

class Clientes(models.Model):
	name = models.CharField(max_length=80)
	country = models.CharField(max_length=30)
	city = models.CharField(max_length=30)
	category = models.CharField(max_length=30)
	user_created = models.CharField(max_length=30)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['name']

class Paises(models.Model):
	name_country = models.CharField(max_length=30)


class Categorias(models.Model):
	name_category = models.CharField(max_length=30)
	num_category = models.IntegerField()