from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TimeSeriesDataViewSet

router = DefaultRouter()
router.register(r'data', TimeSeriesDataViewSet, basename='timeseries')

urlpatterns = [
    path('', include(router.urls)),
]
