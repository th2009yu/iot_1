from django.db import models
#
# Create your models here.
# class agri(models.Model):
#     id = models.IntegerField(primary_key=True)
#     temperature = models.FloatField()
#     humanity = models.FloatField()
#     illumination = models.SmallIntegerField()
#     time = models.BigIntegerField()


# 拥有者
class Owner(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name


# 大棚
class Area(models.Model):
    """
    类型
    编号
    拥有者
    """
    type = models.CharField(max_length=100)
    number = models.IntegerField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)

    class Meta:
        ordering = ('type', 'number',)


# 田野
class Field(models.Model):
    """
    编号
    土壤温度
    土壤湿度
    土壤电导率
    土壤盐度
    空气温度
    空气湿度
    二氧化碳浓度
    土壤ph值
    光照强度
    氧气浓度
    气压
    数据产生时间
    """
    number = models.IntegerField()
    soil_Temperature = models.CharField(max_length=100)
    soil_Humidity = models.CharField(max_length=100)
    soil_Conductivity = models.CharField(max_length=100)
    soil_Salinity = models.CharField(max_length=100)
    air_Temperature = models.CharField(max_length=100)
    air_Humidity = models.CharField(max_length=100)
    carbonDioxide_Concentration = models.CharField(max_length=100)
    soil_PH = models.CharField(max_length=100)
    light_Intensity = models.CharField(max_length=100)
    oxygen_Concentration = models.CharField(max_length=100)
    air_Pressure = models.CharField(max_length=100)
    created = models.CharField(max_length=100)

    class Meta:
        ordering = ('number', 'created', )


# 池塘
class Pond(models.Model):
    """
    编号
    液体温度
    液体溶解氧浓度
    液体ph值
    光照强度
    气压
    数据产生时间
    """
    number = models.IntegerField()
    liquid_Temperature = models.CharField(max_length=100)
    liquidDissolved_OxygenConcentration = models.CharField(max_length=100)
    liquid_PH = models.CharField(max_length=100)
    light_Intensity = models.CharField(max_length=100)
    air_Pressure = models.CharField(max_length=100)
    created = models.CharField(max_length=100)

    class Meta:
        ordering = ('number', 'created',)


# 山林
class Forest(models.Model):
    """
    编号
    土壤温度
    土壤湿度
    土壤电导率
    土壤盐度
    空气温度
    空气湿度
    二氧化碳浓度
    土壤ph值
    光照强度
    风速
    气压
    数据产生时间
    """
    number = models.IntegerField()
    soil_Temperature = models.CharField(max_length=100)
    soil_Humidity = models.CharField(max_length=100)
    soil_Conductivity = models.CharField(max_length=100)
    soil_Salinity = models.CharField(max_length=100)
    air_Temperature = models.CharField(max_length=100)
    air_Humidity = models.CharField(max_length=100)
    carbonDioxide_Concentration = models.CharField(max_length=100)
    soil_PH = models.CharField(max_length=100)
    light_Intensity = models.CharField(max_length=100)
    wind_Speed = models.CharField(max_length=100)
    air_Pressure = models.CharField(max_length=100)
    created = models.CharField(max_length=100)

    class Meta:
        ordering = ('number', 'created',)

