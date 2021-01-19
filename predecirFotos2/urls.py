from rest_framework import routers
from predecirFotos2.views import PersonajesViewSet

router = routers.SimpleRouter()
router.register('predecirF', PersonajesViewSet)

urlpatterns = router.urls