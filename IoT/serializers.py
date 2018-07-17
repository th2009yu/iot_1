from rest_framework import serializers
# from IoT.models import agri
from IoT.models import Owner
from IoT.models import Area
from IoT.models import Field, Pond, Forest

# class agriSerializer(serializers.ModelSerializer):
#     class Meta:
#         # 制定元数据的model和field
#         model = agri
#         fields = ['id', 'temperature', 'humanity', 'illumination', 'time']


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ['name']


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['type', 'number', 'owner']


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ['number', 'soil_Temperature', 'soil_Humidity', 'soil_Conductivity',
                  'soil_Salinity', 'air_Temperature', 'air_Humidity', 'carbonDioxide_Concentration',
                  'soil_PH', 'light_Intensity', 'oxygen_Concentration', 'air_Pressure', 'created']


class PondSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pond
        fields = ['number', 'liquid_Temperature', 'liquidDissolved_OxygenConcentration', 'liquid_PH',
                  'light_Intensity', 'air_Pressure', 'created']


class ForestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forest
        fields = ['number', 'soil_Temperature', 'soil_Humidity', 'soil_Conductivity',
                  'soil_Salinity', 'air_Temperature', 'air_Humidity', 'carbonDioxide_Concentration',
                  'soil_PH', 'light_Intensity', 'wind_Speed', 'air_Pressure', 'created']