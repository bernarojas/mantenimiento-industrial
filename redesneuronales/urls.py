from django.contrib import admin
from django.urls import path
from predecirFotos import InicioWeb, TesteoFallas2

urlpatterns = [
    path('admin/', admin.site.urls),
    path('DatosExcel.html/', InicioWeb.InicioExcel.as_view()), # Carga de datos
    path('previaResultadosExcel.html/', InicioWeb.CargaWebExcel), # NO BORRAR
    path('resultadoTesteo2.html/', TesteoFallas2.Prediccion_fallas2), # Home
]