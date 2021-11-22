"""CRUD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from turing.views import list_view, get_results, upload_file
from turing.views import list_view_informe, get_results_informe, export_csv


urlpatterns = [
    path('admin/', admin.site.urls),
    path('clientes/', list_view, name='clientes'),
    path('clientes/results/', get_results, name='results'),
    re_path(r'^upload/$', upload_file, name="upload_csv"),
    re_path(r'^informe/$', list_view_informe, name="informe"),
    re_path(r'^informe/results_informe/$', get_results_informe, name="result_informe"),
    re_path(r'^results_informe/export/$', export_csv, name="export_csv"),
]