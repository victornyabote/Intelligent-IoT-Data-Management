from rest_framework import viewsets
from .models import TimeSeriesData
from .serializers import TimeSeriesDataSerializer

class TimeSeriesDataViewSet(viewsets.ModelViewSet):
    queryset = TimeSeriesData.objects.all().order_by('timestamp')  # sort by time
    serializer_class = TimeSeriesDataSerializer
