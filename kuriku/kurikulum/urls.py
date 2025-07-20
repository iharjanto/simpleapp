from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MatakuliahViewSet, CPMKViewSet, CPLViewSet, MatakuliahCPLViewSet, SubCPMKViewSet

router = DefaultRouter()
router.register(r'matakuliah', MatakuliahViewSet)
router.register(r'cpmk', CPMKViewSet)
router.register(r'cpl', CPLViewSet)
router.register(r'mkcpl', MatakuliahCPLViewSet)
router.register(r'subcpmk', SubCPMKViewSet)


urlpatterns = [
    path('', include(router.urls)),
]