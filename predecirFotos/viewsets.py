from rest_framework import viewsets
import numpy as np 
import tensorflow as tf

from rest_framework import generics
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

from .models import Book
from .serializer import predecirFotosSerializer

from django.http.response import JsonResponse
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_protect
from rest_framework.views import APIView

@ensure_csrf_cookie
def index2(request):
    #titulox=request.get["data.fields.title"]
    #descri=request.get["data.fields.description"]
    #print(request.get["data.fields.title"])
    #print(request.get["data.fields.description"])
    #guardar=Book(title=titulox, description=descri)
    #guardar.save()
    #print(request.post["fields.title"])
    return render(request, 'index.html')
    #return HttpResponse("")

def games(request):
    book = serialize("json", Book.objects.all())
    #print("Chaoxxxx")
    return HttpResponse(book, content_type="application/json")


class ImagenesBuscadasViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = predecirFotosSerializer


class ImagenesBuscadasViewSet2(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = predecirFotosSerializer


class ImagenesBuscadasViewSet3(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = predecirFotosSerializer
