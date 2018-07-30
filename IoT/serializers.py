from rest_framework import serializers
from django.contrib.auth.models import User
from IoT.models import *


# 用户注册序列化
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')


# 用户列表序列化
class UserSerializer(serializers.ModelSerializer):
    areas = serializers.PrimaryKeyRelatedField(many=True, queryset=Area.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'areas')


# 用户新建序列化
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')


# 大棚（区域）序列化
class AreaSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Area
        fields = ('number', 'detail', 'longitude', 'latitude', 'status', 'owner', 'SoilTemp_max',
                  'SoilTemp_min', 'SoilHumidity_min', 'LightIntensity_min', 'O2C_min',
                  'CO2C_min', 'limit',)


# Arduino类型序列化
class KindOfArduinoSerializer(serializers.ModelSerializer):
    class Meta:
        model = KindOfArduino
        fields = ('kind',)


# 设备序列化
class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('Area_number', 'Rbp_number', 'Ard_number', 'kind',)


# iot数据的序列化
class AgriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agri
        fields = ['Ard_number', 'soil_Humidity', 'soil_Temp',
                  'soil_Salinity', 'soil_EC', 'air_Humidity', 'air_Temp', 'CO2_Concentration',
                  'light_Intensity', 'soil_PH', 'air_Pressure', 'wind_Speed', 'O2_Concentration',
                  'created']


# # 设备（树莓派+Arduino）序列化
# class ArduinoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Arduino
#         fields = ('number', 'kind',)
#
#
# class RaspberryPiSerializer(serializers.ModelSerializer):
#     arduinos = ArduinoSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = RaspberryPi
#         fields = ('number', 'arduinos',)
#