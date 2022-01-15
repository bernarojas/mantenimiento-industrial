import django_filters
from django_filters import DateFilter,CharFilter,DateTimeFilter,NumberFilter

from .models import *

class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="Fecha", lookup_expr='gte')
    end_date = DateFilter(field_name="Fecha", lookup_expr='lte')
    datetime__start = DateTimeFilter(field_name="Fecha", lookup_expr='gte')
    datetime__end = DateTimeFilter(field_name="Fecha", lookup_expr='lte')
    Velocidad__start = NumberFilter(field_name="Velocidad", lookup_expr='gte')

    class Meta:
        model = Sensores_excel
        fields = '__all__'
        exclude = ['Equipo1','Temperatura','Aceleracion','Velocidad_vibracion']

class OrderFilterFechas(django_filters.FilterSet):
    #fecha_exacta = DateTimeFilter(field_name="Fecha", lookup_expr='icontains')
    fecha_exacta = DateTimeFilter(field_name="Fecha", lookup_expr='lte')
    #end_date = DateTimeFilter(field_name="Fecha", lookup_expr='lte')

    class Meta:
        model = SENSORES
        fields = '__all__'
        exclude = ['Presion_agua_sello', 'Flujo_agua_sello', 'Velocidad', 'Flujo_transmisor', 'Densimetro_nuclear', 'Temperatura'
                    , 'Aceleracion', 'Velocidad_vibracion', 'Ingreso', 'Falla', 'Fecha']


