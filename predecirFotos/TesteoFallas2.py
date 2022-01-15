from django.http import HttpResponse
import datetime
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render
from django.views.generic import TemplateView
from .filters import OrderFilterFechas
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model
from predecirFotos.models import EQUIPOSCOLOSO, SENSORES, FALLAS, SENSORESFALLAS
import os
import matplotlib.pyplot as plt
import tensorflow as tf
import collections
from django.db.models import Count

def Prediccion_fallas2(request):
            #RED NEURONAL PROFUNDA
            modelo='./modelos/modeloFallas.h5'
            pesos='./modelos/pesosFallas.h5'
            model = load_model(modelo)
            model.load_weights(pesos)


            class_names = ['Correcto funcionamiento', 'Fuga / Filtracion Ducto descarga', 'Falla de lubricación', 'Falla de rodamientos',
                              'Detención por falla de rodamientos eje motor trabado', 'Desalineamiento',
                              'Desalineamiento más desgaste de correas', 'Corte de correas', 'Alerta de vibración / revisar causa',
                              'Soltura no vinculada a rodamiento', 'Soltura falla inminente de componente', 'Falla de componente']

            #Guarda las fallas declaradas anteriormente en la tabla predecirFotos_fallas
            for e in range(0, 12):
                FALLAS.objects.get_or_create(Nombre_falla=class_names[e])

            #Crea un equipo en la tabla predecirFotos_equiposcoloso
            EQUIPOSCOLOSO.objects.get_or_create(Nombre_equipo='Bomba 501', Descripcion='ESP3 - Baja Densidad',
                                          Tipo_equipo='PTO.BOMBA')


            ultDatIngSens = SENSORES.objects.order_by('-Fecha')[:1]
            myFilter2 = OrderFilterFechas(request.GET, queryset=SENSORES.objects.all())
            ultDatIngSens = myFilter2.qs

            for ultDatIngSens in ultDatIngSens:
              predict_dataset = tf.convert_to_tensor([
              [1, float(ultDatIngSens.Presion_agua_sello), float(ultDatIngSens.Flujo_agua_sello), float(ultDatIngSens.Velocidad), float(ultDatIngSens.Flujo_transmisor), float(ultDatIngSens.Densimetro_nuclear), float(ultDatIngSens.Temperatura), float(ultDatIngSens.Aceleracion), float(ultDatIngSens.Velocidad_vibracion)]
              #[1, 687.03, 5.23, 54.87, 165.26, 1.86, 2.789952, 18.17466, 31.375] #Correcto Funcionamiento
              #[1, 685.84, 5.19, 65.73, 202.03, 1.71, 12.945, 40.155, 35.315] #Soltura no vinculada a rodamiento
              #[1, 692.4, 3.6, 29.33, 2.53, 1.86, 3.903822, 14.67916, 35.3125] # Fuga / Filtracion Ducto descarga
              #[1, 839.84, 8.69, 58.73, 180.2, 1.98, 3.739761, 15.98759, 32.875] #Desalineamiento
              #[1, 685.84, 5.19, 0.0, 0.0, 1.71, 14.43642, 43.9055, 35.51] # Falla de Componente
              ])

            predictions = model(predict_dataset, training=False)

            porcentajes = []
            for i, logits in enumerate(predictions):
                  class_idx = tf.argmax(logits).numpy()
                  p = tf.nn.softmax(logits)[class_idx]
                  for j in range(0, 12):
                        t = tf.nn.softmax(logits)[j]
                        nombre = class_names[j]
                        porcentajes.append(["{:4.1f}".format(100*t), nombre])
                  name = class_names[class_idx]
                  porcentajes.sort()
                  porcentajes.reverse()
                  porcentajeActual=["{:4.1f}".format(100*p),name]


            for f in range(0, 12):
                  idFallas=FALLAS.objects.filter(Nombre_falla__icontains=porcentajes[f][1])
                  SENSORESFALLAS.objects.get_or_create(Porc_falla=porcentajes[f][0],
                                                Fallas_id=idFallas[0].Codigo_f, Sensores_id=ultDatIngSens.Fecha)

            # DATOS RADAR
            datosRadar = SENSORES.objects.order_by('-Fecha')[:5]
            myFilter2 = OrderFilterFechas(request.GET, queryset=SENSORES.objects.order_by('-Fecha'))
            datosRadar = myFilter2.qs[:5]

            #Grafícos de barras
            Fecha = SENSORES.objects.values_list("Fecha", flat=True)
            FilterFecha = OrderFilterFechas(request.GET, queryset=Fecha)
            FilterFecha2 = OrderFilterFechas(request.GET,SENSORES.objects.values_list("Fecha", flat=True).order_by('Fecha'))

            Fecha = FilterFecha.qs
            Fecha_zoom_graph = FilterFecha.qs[::1][-10:]


            #Presión agua sello
            Presion_agua_sello = SENSORES.objects.values_list("Presion_agua_sello", flat=True)
            FilterPresion = OrderFilterFechas(request.GET, queryset=Presion_agua_sello)
            Presion_agua_sello = FilterPresion.qs
            Presion_agua_sello_zoom_graph = FilterPresion.qs[::1][-10:] #.order_by('Presion_agua_sello') #[::-1][:100] #.order_by('-id')[:10][::-1]

            PromedioPresionAguaSello = np.mean(Presion_agua_sello)
            desviacionEstandarPresionAguaSello = np.std(Presion_agua_sello)
            desviacionEstandarPresionAguaSelloSup = PromedioPresionAguaSello + desviacionEstandarPresionAguaSello
            desviacionEstandarPresionAguaSelloInf = PromedioPresionAguaSello - desviacionEstandarPresionAguaSello
            Presion_agua_sello_ordenado = Presion_agua_sello.order_by('Presion_agua_sello')
            FrecuenciaPresionAguaSello = collections.Counter(Presion_agua_sello_ordenado)

            #FLUJO AGUA SELLO
            Flujo_agua_sello = SENSORES.objects.values_list("Flujo_agua_sello", flat=True)
            FilterFlujo = OrderFilterFechas(request.GET, queryset=Flujo_agua_sello)
            Flujo_agua_sello = FilterFlujo.qs
            Flujo_agua_sello_zoom_graph = Flujo_agua_sello[::1][-10:]

            PromedioFlujoAguaSello = np.mean(Flujo_agua_sello)
            desviacionEstandarFlujoAguaSello = np.std(Flujo_agua_sello)
            desviacionEstandarFlujoAguaSelloSup = PromedioFlujoAguaSello + desviacionEstandarFlujoAguaSello
            desviacionEstandarFlujoAguaSelloInf = PromedioFlujoAguaSello - desviacionEstandarFlujoAguaSello
            Flujo_agua_sello_ordenado = Flujo_agua_sello.order_by('Flujo_agua_sello')
            FrecuenciaFlujoAguaSello = collections.Counter(Flujo_agua_sello_ordenado)
            
            #Velocidad
            Velocidad = SENSORES.objects.values_list("Velocidad", flat=True)
            FilterPresion = OrderFilterFechas(request.GET, queryset=Velocidad)
            Velocidad = FilterPresion.qs
            Velocidad_zoom_graph = Velocidad[::1][-10:]

            PromedioVelocidad= np.mean(Velocidad)
            desviacionEstandarVelocidad = np.std(Velocidad)
            desviacionEstandarVelocidadSup = PromedioVelocidad + desviacionEstandarVelocidad
            desviacionEstandarVelocidadInf = PromedioVelocidad - desviacionEstandarVelocidad
            Velocidad_ordenado = Velocidad.order_by('Velocidad')
            FrecuenciaVelocidad = collections.Counter(Velocidad_ordenado)

            #Flujo Transmisor
            Flujo_transmisor = SENSORES.objects.values_list("Flujo_transmisor", flat=True)
            FilterPresion = OrderFilterFechas(request.GET, queryset=Flujo_transmisor)
            Flujo_transmisor = FilterPresion.qs
            Flujo_transmisor_zoom_graph = Flujo_transmisor[::1][-10:]

            PromedioFlujoTransmisor= np.mean(Flujo_transmisor)
            desviacionEstandarFlujoTransmisor = np.std(Flujo_transmisor)
            desviacionEstandarFlujoTransmisorSup = PromedioFlujoTransmisor + desviacionEstandarFlujoTransmisor
            desviacionEstandarFlujoTransmisorInf = PromedioFlujoTransmisor - desviacionEstandarFlujoTransmisor
            Flujo_transmisor_ordenado = Flujo_transmisor.order_by('Flujo_transmisor')
            FrecuenciaFlujo_transmisor = collections.Counter(Flujo_transmisor_ordenado)

            #Densimetro Nuclear
            Densimetro_nuclear = SENSORES.objects.values_list("Densimetro_nuclear", flat=True)
            FilterPresion = OrderFilterFechas(request.GET, queryset=Densimetro_nuclear)
            Densimetro_nuclear = FilterPresion.qs
            Densimetro_nuclear_zoom_graph = Densimetro_nuclear[::1][-10:]

            PromedioDensimetroNuclear= np.mean(Densimetro_nuclear)
            desviacionEstandarDensimetroNuclear = np.std(Densimetro_nuclear)
            desviacionEstandarDensimetroNuclearSup = PromedioDensimetroNuclear + desviacionEstandarDensimetroNuclear
            desviacionEstandarDensimetroNuclearInf = PromedioDensimetroNuclear - desviacionEstandarDensimetroNuclear
            Densimetro_nuclear_ordenado = Densimetro_nuclear.order_by('Densimetro_nuclear')
            FrecuenciaDensimetro_nuclear = collections.Counter(Densimetro_nuclear_ordenado)

            #Temperatura
            Temperatura = SENSORES.objects.values_list("Temperatura", flat=True)
            FilterPresion = OrderFilterFechas(request.GET, queryset=Temperatura)
            Temperatura = FilterPresion.qs
            Temperatura_zoom_graph = Temperatura[::1][-10:]

            PromedioTemperatura= np.mean(Temperatura)
            desviacionEstandarTemperatura = np.std(Temperatura)
            desviacionEstandarTemperaturaSup = PromedioTemperatura + desviacionEstandarTemperatura
            desviacionEstandarTemperaturaInf = PromedioTemperatura - desviacionEstandarTemperatura
            Temperatura_ordenado = Temperatura.order_by('Temperatura')
            FrecuenciaTemperatura = collections.Counter(Temperatura_ordenado)

            #Aceleración
            Aceleracion = SENSORES.objects.values_list("Aceleracion", flat=True)
            FilterPresion = OrderFilterFechas(request.GET, queryset=Aceleracion)
            Aceleracion = FilterPresion.qs
            Aceleracion_zoom_graph = Aceleracion[::1][-10:]

            PromedioAceleracion= np.mean(Aceleracion)
            desviacionEstandarAceleracion = np.std(Aceleracion)
            desviacionEstandarAceleracionSup = PromedioAceleracion + desviacionEstandarAceleracion
            desviacionEstandarAceleracionInf = PromedioAceleracion - desviacionEstandarAceleracion
            Aceleracion_ordenado = Aceleracion.order_by('Aceleracion')
            FrecuenciaAceleracion = collections.Counter(Aceleracion_ordenado)

            #Velocidad Vibración
            Velocidad_vibracion = SENSORES.objects.values_list("Velocidad_vibracion", flat=True)
            FilterPresion = OrderFilterFechas(request.GET, queryset=Velocidad_vibracion)
            Velocidad_vibracion = FilterPresion.qs
            Velocidad_vibracion_zoom_graph = Velocidad_vibracion[::1][-10:]

            PromedioVelocidadVibracion= np.mean(Velocidad_vibracion)
            desviacionEstandarVelocidadVibracion = np.std(Velocidad_vibracion)
            desviacionEstandarVelocidadVibracionSup = PromedioVelocidadVibracion + desviacionEstandarVelocidadVibracion
            desviacionEstandarVelocidadVibracionInf = PromedioVelocidadVibracion - desviacionEstandarVelocidadVibracion
            Velocidad_vibracion_ordenado = Velocidad_vibracion.order_by('Velocidad_vibracion')
            FrecuenciaVelocidad_vibracion = collections.Counter(Velocidad_vibracion_ordenado)

            sensores = SENSORES.objects.values_list("Presion_agua_sello", "Flujo_agua_sello", "Velocidad", "Flujo_transmisor", "Densimetro_nuclear", "Temperatura", "Aceleracion", "Velocidad_vibracion")

            return render(request, "resultadoTesteo2.html", {"porcActual":porcentajeActual[0], "nombActual":porcentajeActual[1],
                                                             "porcentajes":porcentajes, 'myFilter2':myFilter2,
                                                             'Fecha':Fecha,
                                                             'ultDatIngSens':ultDatIngSens, 'datosRadar':datosRadar,
                                                             'Presion_agua_sello':Presion_agua_sello, 'Flujo_agua_sello': Flujo_agua_sello,
                                                             'Velocidad':Velocidad, 'Flujo_transmisor':Flujo_transmisor,
                                                             'Densimetro_nuclear':Densimetro_nuclear, 'Temperatura':Temperatura,
                                                             'Aceleracion':Aceleracion, 'Velocidad_vibracion':Velocidad_vibracion,
                                                             'desviacionEstandarPresionAguaSelloSup':desviacionEstandarPresionAguaSelloSup,
                                                             'desviacionEstandarPresionAguaSelloInf':desviacionEstandarPresionAguaSelloInf,
                                                             'desviacionEstandarFlujoAguaSelloSup':desviacionEstandarFlujoAguaSelloSup,
                                                             'desviacionEstandarFlujoAguaSelloInf':desviacionEstandarFlujoAguaSelloInf,
                                                             'desviacionEstandarVelocidadSup':desviacionEstandarVelocidadSup,
                                                             'desviacionEstandarVelocidadInf':desviacionEstandarVelocidadInf,
                                                             'desviacionEstandarFlujoTransmisorSup':desviacionEstandarFlujoTransmisorSup,
                                                             'desviacionEstandarFlujoTransmisorInf':desviacionEstandarFlujoTransmisorInf,
                                                             'desviacionEstandarDensimetroNuclearSup':desviacionEstandarDensimetroNuclearSup,
                                                             'desviacionEstandarDensimetroNuclearInf':desviacionEstandarDensimetroNuclearInf,
                                                             'desviacionEstandarTemperaturaSup':desviacionEstandarTemperaturaSup,
                                                             'desviacionEstandarTemperaturaInf':desviacionEstandarTemperaturaInf,
                                                             'desviacionEstandarAceleracionSup':desviacionEstandarAceleracionSup,
                                                             'desviacionEstandarAceleracionInf':desviacionEstandarAceleracionInf,
                                                             'desviacionEstandarVelocidadVibracionSup':desviacionEstandarVelocidadVibracionSup,
                                                             'desviacionEstandarVelocidadVibracionInf':desviacionEstandarVelocidadVibracionInf,
                                                             'FrecuenciaPresionAguaSello':FrecuenciaPresionAguaSello.items(),
                                                             'FrecuenciaFlujoAguaSello':FrecuenciaFlujoAguaSello.items(),
                                                             'FrecuenciaVelocidad':FrecuenciaVelocidad.items(),
                                                             'FrecuenciaFlujo_transmisor':FrecuenciaFlujo_transmisor.items(),
                                                             'FrecuenciaDensimetro_nuclear':FrecuenciaDensimetro_nuclear.items(),
                                                             'FrecuenciaTemperatura':FrecuenciaTemperatura.items(),
                                                             'FrecuenciaAceleracion':FrecuenciaAceleracion.items(),
                                                             'FrecuenciaVelocidad_vibracion':FrecuenciaVelocidad_vibracion.items(),
                                                             'Presion_agua_sello_zoom_graph':Presion_agua_sello_zoom_graph,
                                                             'Flujo_agua_sello_zoom_graph':Flujo_agua_sello_zoom_graph,
                                                             'Velocidad_zoom_graph':Velocidad_zoom_graph,
                                                             'Fecha_zoom_graph':Fecha_zoom_graph,
                                                             'Flujo_transmisor_zoom_graph':Flujo_transmisor_zoom_graph,
                                                             'Densimetro_nuclear_zoom_graph':Densimetro_nuclear_zoom_graph,
                                                             'Temperatura_zoom_graph':Temperatura_zoom_graph,
                                                             'Aceleracion_zoom_graph':Aceleracion_zoom_graph,
                                                             'Velocidad_vibracion_zoom_graph':Velocidad_vibracion_zoom_graph,
                                                             'sensores':sensores})