from django.urls import path
from rest_framework import routers
from .viewsets import ImagenesBuscadasViewSet, ImagenesBuscadasViewSet2, index2

router = routers.SimpleRouter()
router.register('api/predecirFotos', ImagenesBuscadasViewSet)
router.register('guardar/predecirFotos', ImagenesBuscadasViewSet2)
urlpatterns = router.urls



#router.register('predecirFotos/', ImagenesBuscadasViewSet)

