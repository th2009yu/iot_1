from rest_framework import serializers
from IoT.models import Owner
from IoT.models import Area
from IoT.models import RaspberryPi
from IoT.models import KindOfArduino
from IoT.models import Arduino
from IoT.models import Agri


# 用户序列化
class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ['name']


# 大棚（区域）序列化
class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['number', 'detail', 'longitude', 'latitude', 'status', 'owner', 'SoilTemp_max',
                  'SoilTemp_min', 'SoilHumidity_min', 'LightIntensity_min', 'O2C_min',
                  'CO2C_min', 'limit']


# 树莓派序列化
class RaspberryPiSerializer(serializers.ModelSerializer):
    class Meta:
        model = RaspberryPi
        fields = ['number', 'belongTo']


# Arduino类型序列化
class KindOfArduinoSerializer(serializers.ModelSerializer):
    class Meta:
        model = KindOfArduino
        fields = ['kind']


# Arduino设备序列化
class ArduinoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arduino
        fields = ['belongToArea', 'belongToRbp', 'number', 'kind']


# Arduino产生数据的序列化
class AgriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agri
        fields = ['belongToArea', 'belongToRbp', 'belongToArd', 'kind', 'soil_Humidity', 'soil_Temp',
                  'soil_Salinity', 'soil_EC', 'air_Humidity', 'air_Temp', 'CO2_Concentration',
                  'light_Intensity', 'soil_PH', 'air_Pressure', 'wind_Speed', 'O2_Concentration',
                  'created']


# class FieldSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Field
#         fields = ['number', 'soil_Temperature', 'soil_Humidity', 'soil_Conductivity',
#                   'soil_Salinity', 'air_Temperature', 'air_Humidity', 'carbonDioxide_Concentration',
#                   'soil_PH', 'light_Intensity', 'oxygen_Concentration', 'air_Pressure', 'created']
#
#
# class PondSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Pond
#         fields = ['number', 'liquid_Temperature', 'liquidDissolved_OxygenConcentration', 'liquid_PH',
#                   'light_Intensity', 'air_Pressure', 'created']
#
#
# class ForestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Forest
#         fields = ['number', 'soil_Temperature', 'soil_Humidity', 'soil_Conductivity',
#                   'soil_Salinity', 'air_Temperature', 'air_Humidity', 'carbonDioxide_Concentration',
#                   'soil_PH', 'light_Intensity', 'wind_Speed', 'air_Pressure', 'created']
