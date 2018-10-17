from django.db import models


# 大棚(区域)
class Area(models.Model):
    """
    编号 [主键]
    名称
    经度
    纬度
    种植作物
    状态
    大棚详细说明 [可选]
    拥有者 [外键]
    温度上限
    温度下限
    温度抖动值
    光照下限
    光照抖动值
    """
    number = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    crops = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default='正常')
    detail = models.CharField(max_length=1000, blank=True)
    owner = models.ForeignKey('auth.User', related_name='areas', on_delete=models.CASCADE)
    temp_max = models.CharField(max_length=100, default='26')
    temp_min = models.CharField(max_length=100, default='20')
    temp_shake = models.CharField(max_length=100, default='1')
    light_min = models.CharField(max_length=100, default='100')
    light_shake = models.CharField(max_length=100, default='80')


# # Arduino类型
# class KindOfArduino(models.Model):
#     """
#     类型 [主键]（1.山林 2.水下 3.田野）
#     """
#     kind = models.CharField(max_length=100, primary_key=True)
#
#     def __str__(self):
#         return self.kind


# 设备
class Device(models.Model):
    """
    Arduino的MAC地址[主键]
    Arduino类型
    该设备在大棚中的坐标x
    该设备在大棚中的坐标y
    Area_number: 所属的大棚（区域）
    """
    Ard_mac = models.CharField(max_length=100, primary_key=True)
    kind = models.CharField(max_length=100, default='未知')
    x = models.CharField(max_length=100)
    y = models.CharField(max_length=100)
    Area_number = models.ForeignKey(Area, related_name='devices', on_delete=models.CASCADE)

    class Meta:
        ordering = ('Area_number', 'Ard_mac')


# iot数据
class Agri(models.Model):
    """
    树莓派MAC地址
    该条数据所属Arduino的MAC地址 [外键]
    树莓派IP地址
    该数据所属大棚编号
    数据所属设备类型
    土壤湿度 [可选]
    土壤湿度 [可选]
    土壤盐度 [可选]
    土壤EC值 [可选]
    空气湿度 [可选]
    空气温度 [可选]
    二氧化碳浓度 [可选]
    光照强度 [可选]
    ph值 [可选]
    气压 [可选]
    风速 [可选]
    氧气浓度 [可选]
    时间
    """
    Rbp_mac = models.CharField(max_length=100)
    Ard_mac = models.ForeignKey(Device, related_name='agris', on_delete=models.CASCADE)
    Rbp_ip = models.CharField(max_length=100)
    Area_number = models.IntegerField()
    kind = models.CharField(max_length=100)
    soil_Humidity = models.CharField(max_length=100, blank=True)
    soil_Temp = models.CharField(max_length=100, blank=True)
    soil_Salinity = models.CharField(max_length=100, blank=True)
    soil_EC = models.CharField(max_length=100, blank=True)
    air_Humidity = models.CharField(max_length=100, blank=True)
    air_Temp = models.CharField(max_length=100, blank=True)
    CO2_Concentration = models.CharField(max_length=100, blank=True)
    light_Intensity = models.CharField(max_length=100, blank=True)
    soil_PH = models.CharField(max_length=100, blank=True)
    air_Pressure = models.CharField(max_length=100, blank=True)
    wind_Speed = models.CharField(max_length=100, blank=True)
    O2_Concentration = models.CharField(max_length=100, blank=True)
    created = models.BigIntegerField()

    class Meta:
        ordering = ('Ard_mac', '-created',)


# 报警记录
class Alarm(models.Model):
    """
    大棚编号
    树莓派的MAC地址
    Arduino的MAC地址
    产生时间
    报警内容
    """
    Area_number = models.IntegerField()
    Rbp_mac = models.CharField(max_length=100)
    Ard_mac = models.CharField(max_length=100, unique=True)
    created = models.CharField(max_length=100)
    content = models.CharField(max_length=100)


# 设备的控制状态
class Control(models.Model):
    """
    Arduino的MAC地址
    灯: (0:关, 1:开)
    温控: (0:关, 1:降, 2:升)
    水泵: (0:关, 1:开)
    风扇: (0:关, 1:开)
    时间
    """
    Ard_mac = models.CharField(max_length=100, unique=True)
    light_control = models.IntegerField()
    temp_control = models.IntegerField()
    waterPump_control = models.IntegerField()
    fan_control = models.IntegerField()
    created = models.BigIntegerField()
