from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render
from predecirFotos.models import EQUIPOSCOLOSO
from django.conf import settings


presionAguaSello = 1
flujoAguaSello = 2
velocidad = 3
flujoTranmisor = 4
densimetroNuclear = 5
temperatura = 6
Aceleracion = 7
VelocidadDeVibracion = 8
GuardarEquipo=EQUIPOSCOLOSO(DESCRIPCION='BOMBA 501, 502 Y 504 JUNTAS', TIPO='BBA501_502_504')
GuardarEquipo.save()

            #equiposBuscados=Equipos.objects.filter(nombre__icontains=equipoBuscar)
