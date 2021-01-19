from django.http import HttpResponse
import datetime
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render

import numpy as np 
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model

from predecirFotos.models import EQUIPOSCOLOSO, SENSORES, FALLAS, SENSORESFALLAS


import os
import matplotlib.pyplot as plt

import tensorflow as tf

def Prediccion_fallas(request):
            #RED NEURONAL PROFUNDA
            modelo='C:/Users/56975/Desktop/ProyectoDjango/redesneuronales/modelos/modeloFallas.h5'
            pesos='C:/Users/56975/Desktop/ProyectoDjango/redesneuronales/modelos/pesosFallas.h5'
            model = load_model(modelo)
            model.load_weights(pesos)

            class_names = ['Correcto funcionamiento', 'Fuga / Filtracion Ducto descarga', 'Falla de lubricación', 'Falla de rodamientos', 
                              'Detención por falla de rodamientos eje motor trabado', 'Desalineamiento', 
                              'Desalineamiento más desgaste de correas', 'Corte de correas', 'Alerta de vibración / revisar causa',
                              'Soltura no vinculada a rodamiento', 'Soltura falla inminente de componente', 'Falla de componente']


            presionAguaSello2 = request.POST["presionAguaSello"]
            flujoAguaSello2 = request.POST["flujoAguaSello"]
            velocidad2 = request.POST["velocidad"]
            flujoTranmisor2 = request.POST["flujoTranmisor"]
            densimetroNuclear2 = request.POST["densimetroNuclear"]
            temperatura2 = request.POST["temperatura"]
            Aceleracion2 = request.POST["Aceleracion"]
            VelocidadDeVibracion2 = request.POST["VelocidadDeVibracion"] 
            #VelocidadDeVibracion2 = tf.constant(request.POST["Aceleracion"], dtype= tf.float64)
            pepito=["{:4}".format(Aceleracion2)]

            #porcentajex = []
            #porcentajex.append([uno, presionAguaSello2, flujoAguaSello2, velocidad2, flujoTranmisor2, densimetroNuclear2, temperatura2, Aceleracion2, VelocidadDeVibracion2])
            #predict_dataset = tf.convert_to_tensor(porcentajex)
            #print(porcentajex)  
            #predictions = model(predict_dataset, training=False)
            predict_dataset = tf.convert_to_tensor([
            [1, float(presionAguaSello2), float(flujoAguaSello2), float(velocidad2), float(flujoTranmisor2), float(densimetroNuclear2), float(temperatura2), float(Aceleracion2), float(VelocidadDeVibracion2)]
            #[1, 687.03, 5.23, 54.87, 165.26, 1.86, 2.789952, 18.17466, 31.375] #Correcto Funcionamiento
            #[1, 685.84, 5.19, 65.73, 202.03, 1.71, 12.945, 40.155, 35.315] #Soltura no vinculada a rodamiento
            #[1, 692.4, 3.6, 29.33, 2.53, 1.86, 3.903822, 14.67916, 35.3125] # Fuga / Filtracion Ducto descarga
            #[1, 839.84, 8.69, 58.73, 180.2, 1.98, 3.739761, 15.98759, 32.875] #Desalineamiento
            #[1, 685.84, 5.19, 0.0, 0.0, 1.71, 14.43642, 43.9055, 35.51] # Falla de Componente
            ])

            predictions = model(predict_dataset, training=False)

            porcentajes = []
            for i, logits in enumerate(predictions):
                  print("numeor de predictions:")
                  print(enumerate(predictions))
                  print("esta es la i:")
                  print("esta es la logits:")
                  print(logits)
                  class_idx = tf.argmax(logits).numpy()
                  print("esta es la class_idx:")
                  print(class_idx)
                  p = tf.nn.softmax(logits)[class_idx]
                  print("esta es la p:")
                  print(p)
                  for j in range(0, 12):
                        t = tf.nn.softmax(logits)[j]
                        nombre = class_names[j]
                        print("{:4.8f}".format(100*t))
                        porcentajes.append(["{:4.1f}".format(100*t), nombre])
                        #porcentajes[j][j]= ["{:4.8f}".format(100*t), nombre]
                  name = class_names[class_idx]
                  print("ES Porcentaje:")
                  print(porcentajes[9][1])
                  porcentajes.sort()
                  porcentajes.reverse()
                  print(porcentajes)

                  print("Example {} prediction: {} ({:4.11f}%)".format(i, name, 100*p))
                  print("Example {} prediction: {} ({:1.11f}%)".format(i, name, p))
                  print("Example {} prediction: {} ({:4.1f}%)".format(i, name, 100*p))

                  porcentajeActual=["{:4.1f}".format(100*p),name]
                  print(porcentajeActual[1])
            #select * from equipos where = 
            presionAguaSello = request.POST["presionAguaSello"]
            flujoAguaSello = request.POST["flujoAguaSello"]
            velocidad = request.POST["velocidad"]
            flujoTranmisor = request.POST["flujoTranmisor"]
            densimetroNuclear = request.POST["densimetroNuclear"]
            temperatura = request.POST["temperatura"]
            Aceleracion = request.POST["Aceleracion"]
            VelocidadDeVibracion = request.POST["VelocidadDeVibracion"]

            GuardarEquipos=EQUIPOSCOLOSO(Nombre_equipo='BBA 501 - 503 - 504', Descripcion='ESP3 - Baja Densidad - BBA 501, 503 Y 504',
                                          Tipo_equipo='PTO.BOMBA')
            GuardarEquipos.save()
            
            
            #for e in range(0, 12):
            #      GuardarFallas=FALLAS(Nombre_falla=class_names[e])
            #      GuardarFallas.save()

            GuardarDatos=SENSORES(Presion_agua_sello=presionAguaSello, Flujo_agua_sello=flujoAguaSello,
                                  Velocidad=velocidad, Flujo_transmisor=flujoTranmisor,
                                 Densimetro_nuclear= densimetroNuclear, Temperatura=temperatura,
                                 Aceleracion=Aceleracion, Velocidad_vibracion=VelocidadDeVibracion,
                                 Equipo_id=1, Ingreso='Automatico')
            GuardarDatos.save()

            #for f in range(0, 12):
            #      GuardarFallas=FALLAS(Nombre_falla=porcentajes[f][1], Porc_falla=porcentajes[f][0], 
            #                           Equipo_id=1, Sensor_id=GuardarDatos.pk)
            #      GuardarFallas.save()

            
            for f in range(0, 12):
                  idFallas=FALLAS.objects.filter(Nombre_falla__icontains=porcentajes[f][1])
                  print("ESTA ES LA FALLA:")
                  print(GuardarDatos.pk)
                  print(idFallas[0].Codigo_f)
                  print(porcentajes[f][0])
                  GuardarFallas=SENSORESFALLAS(Porc_falla=porcentajes[f][0],
                                                Fallas_id=idFallas[0].Codigo_f, Sensores_id=GuardarDatos.pk)
                  GuardarFallas.save()
            

            datosRadar = SENSORES.objects.order_by('-Codigo_s')[:5]
            #for w in range(0, 5):
            #      ("imprimiendo:")
            #      print(datosRadar[w].Codigo_s)

            datosSensores = SENSORES.objects.all()


            return render(request, "resultadoTesteo.html", {"presionAguaSello":presionAguaSello, "flujoAguaSello":flujoAguaSello,
                                    "velocidad":velocidad, "flujoTranmisor":flujoTranmisor, "densimetroNuclear":densimetroNuclear,
                                    "temperatura":temperatura, "Aceleracion":Aceleracion, "VelocidadDeVibracion":VelocidadDeVibracion,
                                    "porcActual":porcentajeActual[0], "nombActual":porcentajeActual[1],
                                    "porcentajes":porcentajes, "datosRadar":datosRadar, "datosSensores":datosSensores})