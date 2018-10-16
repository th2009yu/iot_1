from rest_framework import serializers
from django.contrib.auth.models import User
from IoT.models import *
from rest_framework.validators import UniqueValidator


# 用户注册序列化
class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(label="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])

    password = serializers.CharField(
        style={'input_type': 'password'}, label="密码", write_only=True,
    )

    def create(self, validated_data):
        user = super(UserRegisterSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'password')


# 用户登录序列化
class UserLoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'}, label="密码", write_only=True,
    )

    id = serializers.CharField(label="编号", read_only=True)
    is_staff = serializers.CharField(label="是否是管理员", read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'is_staff')


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
        fields = ('number', 'name', 'longitude', 'latitude', 'crops', 'status', 'detail', 'owner',
                  'temp_max','temp_min', 'temp_shake', 'light_min', 'light_shake',)


# # Arduino类型序列化
# class KindOfArduinoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = KindOfArduino
#         fields = ('kind',)


# 设备序列化
class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Device
        fields = ('Area_number', 'Ard_mac', 'kind', 'x', 'y',)


# iot数据的序列化
class AgriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agri
        fields = ['id', 'Rbp_mac', 'Ard_mac', 'kind', 'soil_Humidity', 'soil_Temp',
                  'soil_Salinity', 'soil_EC', 'air_Humidity', 'air_Temp', 'CO2_Concentration',
                  'light_Intensity', 'soil_PH', 'air_Pressure', 'wind_Speed', 'O2_Concentration',
                  'created']


# 报警记录的序列化
class AlarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alarm
        fields = ['id', 'Area_number', 'Ard_mac', 'created', 'content']


# 设备控制状态的序列化
class ControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Control
        fields = ['Ard_mac', 'light_control', 'temp_control', 'waterPump_control', 'fan']
