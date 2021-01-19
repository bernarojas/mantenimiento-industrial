from django.http import HttpResponse
import datetime
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from openpyxl import load_workbook
from predecirFotos.models import EQUIPOSCOLOSO, Sensores_excel, SENSORES
from datetime import datetime
import matplotlib.pyplot as plt
from django.utils import timezone
import dateutil.parser
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from .filters import OrderFilter
import numpy as np
from numpy import array
from pytz.exceptions import AmbiguousTimeError
import collections
import os
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from scipy.stats import spearmanr

class InicioExcel(TemplateView):
    template_name = 'DatosExcel.html'

def CargaWebExcel(request):
    #SENSORES.objects.all().delete()
    #Sensores_excel.objects.all().delete()
    if request.POST["equipoSelect"] == '4':
        EQUIPOSCOLOSO.objects.get_or_create(Nombre_equipo='Bomba 501', Descripcion='ESP3 - Baja Densidad',
                                Tipo_equipo='PTO.BOMBA')
        print("Imprimiendo SELECT:")
        print(request.POST["equipoSelect"])
        Sensores_excel.objects.all().delete()
        Excel = request.FILES["datosExcel"]
        wb = load_workbook(Excel)
        sheet_obj = wb.active
        numeroFilas = sheet_obj.max_row

        for e in range(2, numeroFilas+1):
                        #GuardarSensoresExcel=Sensores_excel( Fecha = sheet_obj.cell(row = e, column = 1).value, 
                        #                                Funcionando = sheet_obj.cell(row = e, column = 2).value,
                        #                                Presion_agua_sello = sheet_obj.cell(row = e, column = 3).value,
                        #                                Flujo_agua_sello = sheet_obj.cell(row = e, column = 4).value,
                        #                                Velocidad = sheet_obj.cell(row = e, column = 5).value,
                        #                                Flujo_transmisor = sheet_obj.cell(row = e, column = 6).value,
                        #                                Densimetro_nuclear = sheet_obj.cell(row = e, column = 7).value,
                        #                               Temperatura = 0, Aceleracion = 0, Velocidad_vibracion = 0, 
                        #                                Equipo1_id= 1) 
                        GuardarSensoresExcel=Sensores_excel.objects.get_or_create( Fecha = sheet_obj.cell(row = e, column = 1).value, 
                                                        Funcionando = sheet_obj.cell(row = e, column = 2).value,
                                                        Presion_agua_sello = sheet_obj.cell(row = e, column = 3).value,
                                                        Flujo_agua_sello = sheet_obj.cell(row = e, column = 4).value,
                                                        Velocidad = sheet_obj.cell(row = e, column = 5).value,
                                                        Flujo_transmisor = sheet_obj.cell(row = e, column = 6).value,
                                                        Densimetro_nuclear = sheet_obj.cell(row = e, column = 7).value,
                                                        Temperatura = 0, Aceleracion = 0, Velocidad_vibracion = 0, 
                                                        Equipo1_id= 1)
                        #GuardarSensoresExcel.save()

    if request.POST["equipoSelect"] == '1':
        EQUIPOSCOLOSO.objects.get_or_create(Nombre_equipo='Bomba 501', Descripcion='ESP3 - Baja Densidad',
                                            Tipo_equipo='PTO.BOMBA')
        print("Imprimiendo SELECT:")
        print(request.POST["equipoSelect"])
        SENSORES.objects.all().delete()
        Excel = request.FILES["datosExcel"]
        wb = load_workbook(Excel)
        sheet_obj = wb.active
        numeroFilas = sheet_obj.max_row

        for e in range(2, numeroFilas+1):
                    GuardarSensoresExcel=SENSORES.objects.get_or_create( Fecha = sheet_obj.cell(row = e, column = 1).value, 
                                                        Presion_agua_sello = sheet_obj.cell(row = e, column = 3).value,
                                                        Flujo_agua_sello = sheet_obj.cell(row = e, column = 4).value,
                                                        Velocidad = sheet_obj.cell(row = e, column = 5).value,
                                                        Flujo_transmisor = sheet_obj.cell(row = e, column = 6).value,
                                                        Densimetro_nuclear = sheet_obj.cell(row = e, column = 7).value,
                                                        Temperatura = sheet_obj.cell(row = e, column = 8).value, 
                                                        Aceleracion = sheet_obj.cell(row = e, column = 9).value,
                                                        Velocidad_vibracion = sheet_obj.cell(row = e, column = 10).value, 
                                                        Equipo_id= 1, Ingreso = 'Manual')
                    #GuardarSensoresExcel.save()                     
    return redirect('resultadosExcel')
    #return HttpResponseRedirect('resultadosExcel')
    #return render(request, 'resultadosExcel.html', {'datosExcel':datosExcel})
        
        
def VisualizacionExcel(request):
    print("ALALALALALALALLAAAAAAAAAAAAAAAAAAAAAAAAAA")
    datosExcel = Sensores_excel.objects.all()
    #print(datosExcel.Fecha.all())
    #print(datosExcel.Fecha)
    #print(datosExcel[Fecha])
    #print(datosExcel.values.Funcionando)
    myFilter = OrderFilter(request.GET, queryset=datosExcel)
    datosExcel = myFilter.qs
    print("QUE ESSSSSSSSSSSSSSSSSSSSSSS:--")
    print(type(datosExcel))

    datosPresionAguaSello = []
    for datosExcel1 in datosExcel:
        datosPresionAguaSello.append(datosExcel1.Presion_agua_sello)
    PromedioPresionAguaSello = np.mean(datosPresionAguaSello)
    desviacionEstandarPresionAguaSello = np.std(datosPresionAguaSello)
    desviacionEstandarPresionAguaSelloSup = PromedioPresionAguaSello + desviacionEstandarPresionAguaSello
    desviacionEstandarPresionAguaSelloInf = PromedioPresionAguaSello - desviacionEstandarPresionAguaSello
    print("QUE ESSSSSSSSSSSSSSSSSSSSSSS:--")
    print(type(datosPresionAguaSello))
    datosPresionAguaSello.sort()
    distribucionPresionAguaSello = collections.Counter(datosPresionAguaSello)
    distribucionOrdenadaPresionAguaSello = sorted(distribucionPresionAguaSello.items(),key = lambda x: x[1])
    #distribucionOrdenadaPresionAguaSello = sorted(distribucionPresionAguaSello.items(),key = lambda x: x[1], reverse=True)

    datosFlujoAguaSello = []
    for datosExcel1 in datosExcel:
        datosFlujoAguaSello.append(datosExcel1.Flujo_agua_sello)
    PromedioFlujoAguaSello = np.mean(datosFlujoAguaSello)
    desviacionEstandarFlujoAguaSello = np.std(datosFlujoAguaSello)
    desviacionEstandarFlujoAguaSelloSup = PromedioFlujoAguaSello + desviacionEstandarFlujoAguaSello
    desviacionEstandarFlujoAguaSelloInf = PromedioFlujoAguaSello - desviacionEstandarFlujoAguaSello
    
    datosVelocidad = []
    for datosExcel1 in datosExcel:
        datosVelocidad.append(datosExcel1.Velocidad)
    PromedioVelocidad = np.mean(datosVelocidad)
    desviacionEstandarVelocidad = np.std(datosVelocidad)
    desviacionEstandarVelocidadSup = PromedioVelocidad + desviacionEstandarVelocidad
    desviacionEstandarVelocidadInf = PromedioVelocidad - desviacionEstandarVelocidad

    datosFlujoTransmisor = []
    datosFlujoTransmisor2 = array([])
    datosFlujoTransmisor3 = np.array([])
    for datosExcel1 in datosExcel:
        datosFlujoTransmisor.append(datosExcel1.Flujo_transmisor)
        datosFlujoTransmisor2 = np.append(datosFlujoTransmisor2, datosExcel1.Flujo_transmisor)
        datosFlujoTransmisor3 = np.append(datosFlujoTransmisor3, datosExcel1.Flujo_transmisor)
    PromedioFlujoTransmisor = np.mean(datosFlujoTransmisor)
    desviacionEstandarFlujoTransmisor = np.std(datosFlujoTransmisor)
    desviacionEstandarFlujoTransmisorSup = PromedioFlujoTransmisor + desviacionEstandarFlujoTransmisor
    desviacionEstandarFlujoTransmisorInf = PromedioFlujoTransmisor - desviacionEstandarFlujoTransmisor

    datosDensimetroNuclear = []
    for datosExcel1 in datosExcel:
        datosDensimetroNuclear.append(datosExcel1.Densimetro_nuclear)
    PromedioDensimetroNuclear = np.mean(datosDensimetroNuclear)
    desviacionEstandarDensimetroNuclear = np.std(datosDensimetroNuclear)
    desviacionEstandarDensimetroNuclearSup = PromedioDensimetroNuclear + desviacionEstandarDensimetroNuclear
    desviacionEstandarDensimetroNuclearInf = PromedioDensimetroNuclear - desviacionEstandarDensimetroNuclear

    #corr, _ = pearsonr(datosFlujoAguaSello, datosPresionAguaSello)
    #print('Pearsons correlation: %.3f' % corr)
    corrFlujoPresionAguaSello, _ = spearmanr(datosPresionAguaSello, datosFlujoAguaSello)
    corrPresionAguaSelloVelocidad, _ = spearmanr(datosPresionAguaSello, datosVelocidad)
    corrPresionAguaSelloFlujoTransmisor, _ = spearmanr(datosPresionAguaSello, datosFlujoTransmisor)
    corrPresionAguaSelloDensimetroNuclear, _ = spearmanr(datosPresionAguaSello, datosDensimetroNuclear)
    corrFlujoAguaSelloVelocidad, _ = spearmanr(datosFlujoAguaSello, datosVelocidad)
    corrFlujoAguaSelloFlujoTransmisor, _ = spearmanr(datosFlujoAguaSello, datosFlujoTransmisor)
    corrFlujoAguaSelloDensimetroNuclear, _ = spearmanr(datosFlujoAguaSello, datosDensimetroNuclear)
    corrVelocidadFlujoTransmisor, _ = spearmanr(datosVelocidad, datosFlujoTransmisor)
    corrVelocidadDensimetroNuclear, _ = spearmanr(datosVelocidad, datosDensimetroNuclear)
    corrFlujoTransmisorDensimetroNuclear, _ = spearmanr(datosFlujoTransmisor, datosDensimetroNuclear)
    print('Spearmans correlation: %.3f' % corrFlujoPresionAguaSello)
    print("FIAAAAA:", type(datosFlujoTransmisor2))
    print("FIAAAAA:", type(datosFlujoTransmisor3))
    #print(datosFlujoTransmisor2)
    #for i in datosFlujoTransmisor2:
    #    print(i)

    if "buscar" in request.POST:
            print("ESTOY EN BUSCARRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR")
            return render(request, 'resultadosExcel.html')
    return render(request, 'resultadosExcel.html', {'datosExcel':datosExcel, 'myFilter':myFilter,
                                                    'desviacionEstandarPresionAguaSelloSup':desviacionEstandarPresionAguaSelloSup, 
                                                    'desviacionEstandarPresionAguaSelloInf':desviacionEstandarPresionAguaSelloInf,
                                                    'distribucionPresionAguaSello':distribucionPresionAguaSello.items(),
                                                    'distribucionOrdenadaPresionAguaSello':distribucionOrdenadaPresionAguaSello,
                                                    'desviacionEstandarFlujoAguaSelloSup':desviacionEstandarFlujoAguaSelloSup, 
                                                    'desviacionEstandarFlujoAguaSelloInf':desviacionEstandarFlujoAguaSelloInf,
                                                    'desviacionEstandarVelocidadSup':desviacionEstandarVelocidadSup, 
                                                    'desviacionEstandarVelocidadInf':desviacionEstandarVelocidadInf,
                                                    'desviacionEstandarFlujoTransmisorSup':desviacionEstandarFlujoTransmisorSup, 
                                                    'desviacionEstandarFlujoTransmisorInf':desviacionEstandarFlujoTransmisorInf,
                                                    'desviacionEstandarDensimetroNuclearSup':desviacionEstandarDensimetroNuclearSup, 
                                                    'desviacionEstandarDensimetroNuclearInf':desviacionEstandarDensimetroNuclearInf,
                                                    'corrFlujoPresionAguaSello':corrFlujoPresionAguaSello,
                                                    'corrPresionAguaSelloVelocidad':corrPresionAguaSelloVelocidad,
                                                    'corrPresionAguaSelloFlujoTransmisor':corrPresionAguaSelloFlujoTransmisor,
                                                    'corrPresionAguaSelloDensimetroNuclear':corrPresionAguaSelloDensimetroNuclear,
                                                    'corrFlujoAguaSelloVelocidad':corrFlujoAguaSelloVelocidad,
                                                    'corrFlujoAguaSelloFlujoTransmisor':corrFlujoAguaSelloFlujoTransmisor,
                                                    'corrFlujoAguaSelloDensimetroNuclear':corrFlujoAguaSelloDensimetroNuclear,
                                                    'corrVelocidadFlujoTransmisor':corrVelocidadFlujoTransmisor,
                                                    'corrVelocidadDensimetroNuclear':corrVelocidadDensimetroNuclear,
                                                    'corrFlujoTransmisorDensimetroNuclear':corrFlujoTransmisorDensimetroNuclear})



class FiltrosExcel(TemplateView):
    template_name = 'filtros.html'

class iniciarTemplate(TemplateView):
    template_name = 'template.html'

class iniciarTemplate2(TemplateView):
    template_name = 'template2.html'

class iniciarTemplate3(TemplateView):
    template_name = 'Rodolfo.html'

class iniciarTemplate4(TemplateView):
    template_name = 'login.html'

def iniciarWeb(request):

    return render(request, "testeoFallas.html")

