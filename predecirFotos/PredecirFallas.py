from django.http import HttpResponse
import datetime
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render

import numpy as np 
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model


import os
import matplotlib.pyplot as plt

import tensorflow as tf

#RED NEURONAL PROFUNDA
modelo='C:/Users/56975/Desktop/ProyectoDjango/Proyecto1/modelo/modelo.h5'
pesos='C:/Users/56975/Desktop/ProyectoDjango/Proyecto1/modelo/pesos.h5'
model = load_model(modelo)
model.load_weights(pesos)

class_names = ['Bomba con Baja Eficiencia', 'Filtracion Por Carcasa, Junta/Union Bomba', 'Indisponible Bajo Rendimiento / Perdida Eficiencia', 
               'Fuga / Filtracion Plato de Succion Bomba', 'Eje Cortado', 'Correcto Funcionamiento', 'Bomba Detenida']

predict_dataset = tf.convert_to_tensor([
    [1, 861.2, 4.5, 83.8, 81.7, 2.3, 99.4, 941.7],
    [1, 477.1, 26.6, 79.8, 98.8, 2.4, 115.4, 1041.3],
    [1, 471.5, 20.6, 82.8, 110.5, 2.5, 107.8, 1165.6],
    [1, 471.5, 20.6, 82.8, 110.5, 2.5, 107.8, 1165.6],
    [1, 471.5, 20.6, 82.8, 110.5, 2.5, 107.8, 1165.6],
    [1, 471.5, 20.6, 82.8, 110.5, 2.5, 107.8, 1165.6]
])

# training=False is needed only if there are layers with different
# behavior during training versus inference (e.g. Dropout).
predictions = model(predict_dataset, training=False)

ejemplo1 =1
ejemplo2 =1
ejemplo3 =1
ejemplo4 =1
ejemplo5 =1
ejemplo6 =1
prediccion1 = ""
prediccion2 = ""
prediccion3 = ""
prediccion4 = ""
prediccion5 = ""
prediccion6 = ""
probabilidad1 = 1
probabilidad2 = 1
probabilidad3 = 1
probabilidad4 = 1
probabilidad5 = 1
probabilidad6 = 1

for i, logits in enumerate(predictions):
  class_idx = tf.argmax(logits).numpy()
  p = tf.nn.softmax(logits)[class_idx]
  name = class_names[class_idx]
  if i == 0:
    ejemplo1=i
    prediccion1=name
    probabilidad1= "{:4.1f}".format(p*100)
    comentarios1=["Sin Comentario :)"]
  
  if i == 1:
        ejemplo2=i
        prediccion2=name
        probabilidad2= "{:4.1f}".format(p*100)
        comentarios2= "Se desarma bomba, detectando plato de succion con daño considerable, Se repara con Combo Wear, se realiza armado de bomba, pendiente reapriete de pernos carcaza y montar ducto de succion."
  
  if i == 2:
        ejemplo3=i
        prediccion3=name
        probabilidad3= "{:4.1f}".format(p*100)
        ##EJE CORTADO
        comentarios3 = "Cuerpo de rodamiento con eje cortado Se comienza con desmontaje y desarme de componentes, trabajo pendiente por indisponibilidad de repuesto (Bearing) en bodega."

  if i ==3:
        ejemplo4=i
        prediccion4=name
        probabilidad4= "{:4.1f}".format(p*100)
        ##Indisponible Bajo Rendimiento / Perdida Eficiencia:
        comentarios4 = "Se repara plato desgaste con Combowear, se cambia impulsor."

  if i ==4:
        ejemplo5=i
        prediccion5=name
        probabilidad5= "{:4.1f}".format(p*100)
        ##Filtracion Por Carcasa, Junta/Union Bomba
        comentarios5 = "Normalizar BombaPendiente postura de ducto de succion, bba presentó fuga en inspeccion por filtracion , se encuentra dañada en liner de succion. Se realiza cambio de partes humedas liner de succion ,liner de descarga e impulsor."

  if i ==5:
        ejemplo6=i
        prediccion6=name
        probabilidad6= "{:4.1f}".format(p*100)
        ##Bomba con Baja Eficiencia
        comentarios6 = "Se desarma bomba Perno de carcaza, succion y descarga."
  
  print("Example {} prediction: {} ({:4.1f}%)".format(i, name, 100*p))

def Prediccion_fallas(request):
    ahora=datetime.datetime.now()
    return render(request, "predFallas.html", {"ejemplo1":ejemplo1, "ejemplo2":ejemplo2, "ejemplo3":ejemplo3,
                "prediccion1":prediccion1, "prediccion2":prediccion2, "prediccion3":prediccion3, "momento_actual":ahora,
                "probabilidad1":probabilidad1, "probabilidad2":probabilidad2, "probabilidad3":probabilidad3,
                "ejemplo4":ejemplo4, "ejemplo5":ejemplo5, "ejemplo6":ejemplo6,
                "prediccion4":prediccion4, "prediccion5":prediccion5, "prediccion6":prediccion6,
                "probabilidad4":probabilidad4, "probabilidad5":probabilidad5, "probabilidad6":probabilidad6,
                "comentarios1":comentarios1, "comentarios2":comentarios2, "comentarios3":comentarios3,
                "comentarios4":comentarios4, "comentarios5":comentarios5, "comentarios6":comentarios6})