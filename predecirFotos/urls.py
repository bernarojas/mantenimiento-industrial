from django.urls import path
from rest_framework import routers
from .viewsets import games, index2

urlpatterns = [
    path('predecirFotos/', games, name="games"),
    #path('guardar/predecirFotos/', index2, name="index2"),
]

#router.register('predecirFotos/', ImagenesBuscadasViewSet)


"""router = routers.SimpleRouter()
router.register('api/predecirFotos', ImagenesBuscadasViewSet2)
router.register('apa/predecirFotos', ImagenesBuscadasViewSet)


#router.register('predecirFotos', patomar)
urlpatterns = router.urls


urlpatterns = [
    path('api/predecirFotos/', ImagenesBuscadasViewSet),
    path('predecirFotos/', ImagenesBuscadasViewSet),
]
"""
