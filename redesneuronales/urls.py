from django.contrib import admin
from django.urls import path, include

from predecirFotos import InicioWeb, predecirFotos, PredecirFallas, TesteoFallas, TesteoFallas2
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('predecirFotos.urls2')),
    path('apa/', include('predecirFotos.urls')),
    path('apa/', include('predecirFotos.urls2')),
    path('predFotos.html/', predecirFotos.iniciarWeb),
    path('resultadosFoto/', predecirFotos.fotoingresada),
    path('predFallas.html/', PredecirFallas.Prediccion_fallas),
    path('testeoFallas.html/', InicioWeb.iniciarWeb),
    path('resultadoTesteo.html/', TesteoFallas.Prediccion_fallas),
    path('DatosExcel.html/', InicioWeb.InicioExcel.as_view()),
    path('previaResultadosExcel.html/', InicioWeb.CargaWebExcel),
    path('resultadosExcel.html/', InicioWeb.VisualizacionExcel, name = 'resultadosExcel'),
    path('template.html/', InicioWeb.iniciarTemplate.as_view()),
    path('template2.html/', InicioWeb.iniciarTemplate2.as_view()),
    path('resultadoTesteo2.html/', TesteoFallas2.Prediccion_fallas2),
    path('Rodolfo.html/', InicioWeb.iniciarTemplate3.as_view()),
    path('login.html/', InicioWeb.iniciarTemplate4.as_view()),
    #path('filtros.html/', InicioWeb.FiltrosExcel.as_view()),
    #path('api', include('predecirFotos.urls2')),
    #path('/api/predecirFotos/', include('predecirFotos.urls2')),
    #path('/api/predecirFotos', include('predecirFotos.urls2')),
    #path('api/predecirFotos/', include('predecirFotos.urls2')),
    #path('api/predecirFotos', include('predecirFotos.urls2')),
]

    #path('api-auth', include('rest_framework.urls')),
    #path('', include('predecirFotos.urls'))
    #path('predFotos.html/', predecirFotos.iniciarWeb),
    #path('resultadosFoto/', predecirFotos.fotoingresada),
    #path('api/predecirFotos/', include("predecirFotos.urls")),
    #path('predecirFotos/', ImagenesBuscadasViewSet.patomar),
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)