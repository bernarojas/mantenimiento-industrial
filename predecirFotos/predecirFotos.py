import numpy as np
import tensorflow as tf

from django.http import HttpResponse
import datetime
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model

from predecirFotos.models import Equipos, ImagenesBuscadas

from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

longitud, altura = 100, 100
modelo='C:/Users/56975/Pictures/TensorFlow/modelo/modelo.h5'
pesos='C:/Users/56975/Pictures/TensorFlow/modelo/pesos.h5'
cnn = load_model(modelo)
cnn.load_weights(pesos)

animal = ""
animal1 = ""
animal2 = ""
animal3 = ""

def predict(file):
    x=load_img(file, target_size=(longitud, altura))
    x=img_to_array(x)
    x=np.expand_dims(x, axis=0)
    arreglo=cnn.predict(x)
    resultado=arreglo[0]
    respuesta=np.argmax(resultado)
    if respuesta==0:
        animal="bomba"
        print('bomba')
    elif respuesta==1:
        animal="tk"
        print('tk')
    elif respuesta==2:
        animal="Perro"
        print('Perro')
    elif respuesta==3:
        animal="Gorila"
        print('Gorila')
    elif respuesta==4:
        animal="Gato"
        print('Gato')
    return animal



animal2 = predict('C:/Users/56975/Pictures/TensorFlow/gato.jpg')


def iniciarWeb(request):

    return render(request, "predFotos.html")

def fotoingresada(request):
    fecha_actual=datetime.datetime.now()
    print(request.FILES["fotoBuscada"])
    predict(request.FILES["fotoBuscada"])
    foto=request.FILES["fotoBuscada"]
    fs = FileSystemStorage()
    filename = fs.save(foto.name, foto)
    uploaded_file_url = fs.url(filename)
    print(fs)
    print(filename)
    print("holi")
    print(uploaded_file_url)
    print("holi")
    equipoBuscar = predict(request.FILES["fotoBuscada"])
    equiposBuscados=Equipos.objects.filter(nombre__icontains=equipoBuscar)
    print("ES UN...")
    print(equipoBuscar)
    imgGuardarBD=ImagenesBuscadas(fecha=fecha_actual, imagen=foto)
    imgGuardarBD.save()
    print(imgGuardarBD.imagen)
    nombreFotoBd=imgGuardarBD.imagen
    #rodolfo=ImagenesBuscadas.objects.all()
    #print(rodolfo[0].)
    DevuelveFotoSave=ImagenesBuscadas.objects.filter(imagen__icontains=nombreFotoBd)
    #print(fecha_actual)
    return render(request, "resultadosFoto.html", {"equiposBuscados":equiposBuscados, "query":filename, 
                                               "FotoBD": DevuelveFotoSave, "EsUn":equipoBuscar})
    #return render(request, "resultadosFoto.html", {"equiposBuscados":equiposBuscados, "query":foto})
