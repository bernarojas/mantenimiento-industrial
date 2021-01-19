from django.shortcuts import render
from rest_framework import viewsets
from .serializer import PersonajesSerializer
from .models import Personajes

# Create your views here.

class PersonajesViewSet(viewsets.ModelViewSet):
    queryset = Personajes.objects.all()
    serializer_class = PersonajesSerializer
