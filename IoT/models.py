from django.db import models


# 大棚状态
class Status(models.Model):
    """
    大棚状态：正常、警告
    """
    status = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.status


# 大棚(区域)
class Area(models.Model):
    """
    编号 [主键]
    大棚详细说明 [可选]
    经度
    纬度
    状态 [外键]
    拥有者 [外键]
    土壤温度上限
    土壤温度下限
    土壤湿度下限
    光照强度下限
    氧气浓度下限
    二氧化碳浓度下限
    连续多少条数据超过阈值开始控制
    """
    number = models.IntegerField(primary_key=True)
    detail = models.CharField(max_length=1000, blank=True)
    longitude = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', related_name='areas', on_delete=models.CASCADE)
    SoilTemp_max = models.CharField(max_length=100)
    SoilTemp_min = models.CharField(max_length=100)
    SoilHumidity_min = models.CharField(max_length=100)
    LightIntensity_min = models.CharField(max_length=100)
    O2C_min = models.CharField(max_length=100)
    CO2C_min = models.CharField(max_length=100)
    limit = models.IntegerField()


# Arduino类型
class KindOfArduino(models.Model):
    """
    类型 [主键]（1.山林 2.水下 3.田野）
    """
    kind = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.kind


# # 树莓派
# class RaspberryPi(models.Model):
#     """
#     编号 [主键]
#     所属的大棚（区域）[外键]
#     """
#     number = models.IntegerField(primary_key=True)
#     Area_number = models.ForeignKey(Area, related_name='raspberrypis', on_delete=models.CASCADE)
#
#     class Meta:
#         ordering = ('Area_number', 'number',)
#
#
# # Arduino
# class Arduino(models.Model):
#     """
#     所属的树莓派 [外键]
#     Arduino编号 [主键]
#     Arduino类型 [外键]
#     """
#     Rbp_number = models.ForeignKey(RaspberryPi, related_name='arduinos', on_delete=models.CASCADE)
#     number = models.IntegerField(primary_key=True)
#     kind = models.ForeignKey(KindOfArduino, on_delete=models.CASCADE)
#
#     class Meta:
#         ordering = ('Rbp_number', 'number',)


# 设备
class Device(models.Model):
    """
    数量级关系：大棚 1：N 树莓派 1：N arduino
    Rbp_number: 树莓派编号
    Ard_number: arduino编号
    kind: arduino类型
    Area_number: 所属的大棚（区域）
    """
    Rbp_number = models.IntegerField()
    Ard_number = models.IntegerField(primary_key=True)
    kind = models.ForeignKey(KindOfArduino, related_name='devices', on_delete=models.CASCADE)
    Area_number = models.ForeignKey(Area, related_name='devices', on_delete=models.CASCADE)

    class Meta:
        ordering = ('Area_number', 'Rbp_number', 'Ard_number')


# iot数据
class Agri(models.Model):
    """
    所属Arduino编号 [外键]
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
    Ard_number = models.ForeignKey(Device, related_name='agris', on_delete=models.CASCADE)
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
    created = models.CharField(max_length=100)

    class Meta:
        ordering = ('Ard_number', '-created',)
