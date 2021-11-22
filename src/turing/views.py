# Paginator import
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django_hosts.resolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.views.generic import TemplateView
from django.template import loader
import logging
import pandas as pd
import csv, io, json


# import my model
from turing.models import Clientes
from turing.forms import SubmitFile
from turing.validators import handle_upload_file
# Create your views here.



def list_view(request):
	clientes_list = Clientes.objects.all().order_by('name')
	paginator = Paginator(clientes_list, 100)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	return render(request, 'turing/lista_clientes.html', {'page_obj': page_obj})


def get_results(request, name=None, *args, **kwargs):

	if request.GET['name']:
		search = request.GET['name']
		result = Clientes.objects.filter(name__icontains=search)
		return render(request, 'turing/results.html', {'result': result})
	else:
		mensaje = "introduzca un valor de busqueda"

	return HttpResponse(mensaje)


def upload_file(request):
	#data = {}
	template_name = "turing/upload.html"
	data = Clientes.objects.all()
	prompt = {
		'order': 'El orden de el ingreso de informacion debe ser, name, country, city, category',
		'profiles': data
	}
	if request.method == 'GET':
		return render(request, 'turing/upload.html', prompt)

	elif request.method == 'POST':
		csv_file = request.FILES['file']
		if not csv_file.name.endswith('.csv'):
			messages.error(request, 'File not is a csv file')
			#return HttpResponseRedirect(reverse("turing:upload_csv"))
		data_set = csv_file.read().decode('UTF-8')
		#if csv_file.multiple_chunks():
		#	messages.error(request, "Upload file is too big (%.2f MB)." % (csv_file.size/(1000*1000)))
		#	return HttpResponseRedirect(reverse("turing:upload_csv"))
		io_string = io.StringIO(data_set)
		next(io_string)
		for column in csv.reader(io_string, delimiter=","):
			obj, created = Clientes.objects.update_or_create(
							name=column[0], 
							country=column[1], 
							city=column[2], 
							category=column[3]
				)

	context = {}
	return render(request, template_name, context)


def informe_csv(created_at, country, category, city):
	#template_name = 'turing/informe.html'
	#clientes = Clientes.objects.all().values_list('name', 'country', 'city', 'category', 'user_created', 'is_active', 'created_at', 'updated_at')
	response = HttpResponse(
		content_type="text/csv", 
		headers={'Content-Disposition' :  'attachment; filename = "informe.csv"'}
	#response = ['Content-Disposition'] =  'attachment; filename = "informe.csv"'
	)
	csv_writer = csv.writer(response)
	csv_writer.writerow(['name', 'country', 'city', 'category', 'user_created', 'is_active', 'created_at', 'updated_at'])

	if created_at:
		r_created_at = Clientes.objects.filter(name__icontains=created_at)
		for cliente in r_created_at:
			csv_writer.writerow(cliente.name, cliente.country, cliente.category, cliente.user_created, cliente.is_active, cliente.created_at, cliente.updated_at)

	elif country:
		r_country = Clientes.objects.filter(name__icontains=country)
		for cliente in r_country:
			csv_writer.writerow(cliente.name, cliente.country, cliente.category, cliente.user_created, cliente.is_active, cliente.created_at, cliente.updated_at)

	elif category:
		r_category = Clientes.objects.filter(name__icontains=category)
		for cliente in r_category:
			csv_writer.writerow(cliente.name, cliente.country, cliente.category, cliente.user_created, cliente.is_active, cliente.created_at, cliente.updated_at)
			

	elif city:
		r_city = Clientes.objects.filter(name__icontains=city)
		for cliente in r_city:
			csv_writer.writerow(cliente.name, cliente.country, cliente.category, cliente.user_created, cliente.is_active, cliente.created_at, cliente.updated_at)
	else:
		return HttpResponse('No ha introducido ningun valor de busqueda')

	#tem = loader.get_template(template_name)
	#c = {'data': csv_writer}
	#response.write(tem.render(c))
	return response


def list_view_informe(request):
	clientes_list = Clientes.objects.all().order_by('name')
	paginator = Paginator(clientes_list, 100)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	
	"""
		if request.GET.get('created_at'):
			created_at = request.GET['created_at']
			r_created_at = Clientes.objects.filter(name__icontains=created_at)
			for cliente in r_created_at:
				csv_writer.writerow(cliente.name, cliente.country, cliente.category, cliente.user_created, cliente.is_active, cliente.created_at, cliente.updated_at)
			return response
		
		if request.GET.get('country'):
			country = request.GET.get('country')
			r_country = Clientes.objects.filter(name__icontains=country)
			for cliente in r_country:
				csv_writer.writerow(cliente.name, cliente.country, cliente.category, cliente.user_created, cliente.is_active, cliente.created_at, cliente.updated_at)
			return response

		if request.GET.get('category'):
			category = request.GET['category']
			r_category = Clientes.objects.filter(name__icontains=category)
			for cliente in r_category:
				csv_writer.writerow(cliente.name, cliente.country, cliente.category, cliente.user_created, cliente.is_active, cliente.created_at, cliente.updated_at)
			return response

		if request.GET.get('city'):
			city = request.GET['city']
			r_city = Clientes.objects.filter(name__icontains=city)
			for cliente in r_city:
				csv_writer.writerow(cliente.name, cliente.country, cliente.category, cliente.user_created, cliente.is_active, cliente.created_at, cliente.updated_at)
			return response
			#return informe_csv(created_at, country, category, city)
			#return render(request, 'turing/results.html', {'result': result})
	"""	
	return render(request, 'turing/informe.html', {'page_obj': page_obj})
	#return response

def export_csv(request):
	response = HttpResponse(
	content_type="text/csv", 
	headers={'Content-Disposition' :  'attachment; filename = "informe.csv"'}
#response = ['Content-Disposition'] =  'attachment; filename = "informe.csv"'
)
	csv_writer = csv.writer(response)
	csv_writer.writerow(['name', 'country', 'city', 'category', 'user_created', 'is_active', 'created_at', 'updated_at'])



	if not request.GET.get('name'):
		return HttpResponse('Not found')

	created_at = request.GET.get('name')
	r_created_at = Clientes.objects.filter(name__icontains=created_at)
	for cliente in r_created_at:
		csv_writer.writerow(cliente.name, cliente.country, cliente.category, cliente.user_created, cliente.is_active, cliente.created_at, cliente.updated_at)
	return response



def get_results_informe(request, name=None, *args, **kwargs):

	if request.GET['name']:
		search = request.GET['name']
		result = Clientes.objects.filter(name__icontains=search)
		return render(request, 'turing/results_informe.html', {'result': result})