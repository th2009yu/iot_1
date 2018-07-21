from django.db import models


# 拥有者
class Owner(models.Model):
    """
    名字 [主键]
    """
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name


# 状态
class Status(models.Model):
    """
    状态
    """
    status = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.status


# 大棚(区域)
class Area(models.Model):
    """
    编号 [主键]
    细节说明 [可选]
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
    code = ('正常', '警告')

    number = models.IntegerField(primary_key=True)
    detail = models.CharField(max_length=1000, blank=True)
    longitude = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    SoilTemp_max = models.CharField(max_length=100)
    SoilTemp_min = models.CharField(max_length=100)
    SoilHumidity_min = models.CharField(max_length=100)
    LightIntensity_min = models.CharField(max_length=100)
    O2C_min = models.CharField(max_length=100)
    CO2C_min = models.CharField(max_length=100)
    limit = models.IntegerField()


# 树莓派
class RaspberryPi(models.Model):
    """
    编号 [主键]
    所属的大棚（区域）[外键]
    """
    number = models.IntegerField(primary_key=True)
    belongTo = models.ForeignKey(Area, related_name='raspberrypi', on_delete=models.CASCADE)


# Arduino类型
class KindOfArduino(models.Model):
    """
    类型 [主键]
    """
    kind = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.kind


# Arduino
class Arduino(models.Model):
    """
    所属的大棚（区域） [外键]
    所属的树莓派 [外键]
    Arduino编号 [主键]
    Arduino类型（1.山林 2.水下 3.田野）[外键]
    """
    belongToArea = models.ForeignKey(Area, related_name='arduino', on_delete=models.CASCADE)
    belongToRbp = models.ForeignKey(RaspberryPi, related_name='arduino', on_delete=models.CASCADE)
    number = models.IntegerField(primary_key=True)
    kind = models.ForeignKey(KindOfArduino, on_delete=models.CASCADE)

    class Meta:
        ordering = ('belongToArea', 'belongToRbp', 'number',)


# iot数据
class Agri(models.Model):
    """
    1.所属的大棚（区域） [外键]
    所属的树莓派 [外键]
    所属Arduino编号 [外键]
    所属Arduino类型（1.山林 2.水下 3.田野）[外键]
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
    17.时间
    """
    belongToArea = models.ForeignKey(Area, related_name='agri', on_delete=models.CASCADE)
    belongToRbp = models.ForeignKey(RaspberryPi, related_name='agri', on_delete=models.CASCADE)
    belongToArd = models.ForeignKey(Arduino, on_delete=models.CASCADE)
    kind = models.ForeignKey(KindOfArduino, related_name='agri', on_delete=models.CASCADE)
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


# 田野
# class Field(models.Model):
#     """
#     编号
#     土壤温度
#     土壤湿度
#     土壤电导率
#     土壤盐度
#     空气温度
#     空气湿度
#     二氧化碳浓度
#     土壤ph值
#     光照强度
#     氧气浓度
#     气压
#     数据产生时间
#     """
#     number = models.IntegerField()
#     soil_Temperature = models.CharField(max_length=100)
#     soil_Humidity = models.CharField(max_length=100)
#     soil_Conductivity = models.CharField(max_length=100)
#     soil_Salinity = models.CharField(max_length=100)
#     air_Temperature = models.CharField(max_length=100)
#     air_Humidity = models.CharField(max_length=100)
#     carbonDioxide_Concentration = models.CharField(max_length=100)
#     soil_PH = models.CharField(max_length=100)
#     light_Intensity = models.CharField(max_length=100)
#     oxygen_Concentration = models.CharField(max_length=100)
#     air_Pressure = models.CharField(max_length=100)
#     created = models.CharField(max_length=100)
#
#     class Meta:
#         ordering = ('number', 'created', )
#
#
# # 池塘
# class Pond(models.Model):
#     """
#     编号
#     液体温度
#     液体溶解氧浓度
#     液体ph值
#     光照强度
#     气压
#     数据产生时间
#     """
#     number = models.IntegerField()
#     liquid_Temperature = models.CharField(max_length=100)
#     liquidDissolved_OxygenConcentration = models.CharField(max_length=100)
#     liquid_PH = models.CharField(max_length=100)
#     light_Intensity = models.CharField(max_length=100)
#     air_Pressure = models.CharField(max_length=100)
#     created = models.CharField(max_length=100)
#
#     class Meta:
#         ordering = ('number', 'created',)
#
#
# # 山林
# class Forest(models.Model):
#     """
#     编号
#     土壤温度
#     土壤湿度
#     土壤电导率
#     土壤盐度
#     空气温度
#     空气湿度
#     二氧化碳浓度
#     土壤ph值
#     光照强度
#     风速
#     气压
#     **氧气**
#     数据产生时间
#     """
#     number = models.IntegerField()
#     soil_Temperature = models.CharField(max_length=100)
#     soil_Humidity = models.CharField(max_length=100)
#     soil_Conductivity = models.CharField(max_length=100)
#     soil_Salinity = models.CharField(max_length=100)
#     air_Temperature = models.CharField(max_length=100)
#     air_Humidity = models.CharField(max_length=100)
#     carbonDioxide_Concentration = models.CharField(max_length=100)
#     soil_PH = models.CharField(max_length=100)
#     light_Intensity = models.CharField(max_length=100)
#     wind_Speed = models.CharField(max_length=100)
#     air_Pressure = models.CharField(max_length=100)
#     created = models.CharField(max_length=100)
#
#     class Meta:
#         ordering = ('number', 'created',)
