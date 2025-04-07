from rest_framework import serializers
from .models import TimeSeriesData

class TimeSeriesDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSeriesData
        fields = '__all__'
