from .models import Personajes
from rest_framework import serializers


class PersonajesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personajes
        fields = '__all__'
        #fields = ('id','nombre','nombre_real','imagen', 'descripcion')


        