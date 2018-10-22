from __future__ import unicode_literals
from rest_framework.views import APIView
from IoT.permissions import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.http import Http404
from django.http import HttpResponse
import socket, time
from django.contrib.auth import logout, login
import json


# # 客户端命令接口
# def order(request):
#     """
#     receive command from client and send it to the cloud platform
#     :return: command received from client
#     """
#     if request.GET.get('command'):
#         command = request.GET['command']
#         serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         serversocket.sendto(b'ep=23SSMC3PDDQ7T1N7&pw=845962', ('115.29.240.46', 6000))
#         time.sleep(1)
#         serversocket.sendto(command.encode('utf-8'), ('115.29.240.46', 6000))
#         return HttpResponse('send success!')
#     else:
#         return HttpResponse('send failed!')


# 手动控制 (E.g. /order?area_number=1&ard_mac=11111&command=hhh)
def order(request):
    """
    1. Client将 [大棚、节点、操作内容] 发送给Server
    2. Server在【数据】中查找该节点最新对应的树莓派IP
    3. 然后用UDP协议发送给树莓派 [大棚、节点、操作内容]
    """
    if request.GET.get('area_number') and request.GET.get('ard_mac') and request.GET.get('command'):
        Area_number = request.GET['area_number']
        Ard_mac = request.GET['ard_mac']
        Command = request.GET['command']
        data = {
            'Area_number': Area_number,
            'Ard_mac': Ard_mac,
            'Command': Command
        }
        json_data = json.dumps(data, ensure_ascii=False)
        try:
            # 在【Agri】中查找该节点最新对应的树莓派IP
            Rbp_ip = Agri.objects.values("Rbp_ip").filter(Ard_mac=Ard_mac).first()['Rbp_ip']
            # 用UDP协议发送给树莓派 [大棚、节点、操作内容]
            serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            serversocket.sendto(json_data.encode('utf-8'), (Rbp_ip, 7777))
            return HttpResponse('Order send successfully!')
        except TypeError:
            return HttpResponse('Error! Database record does not exist!')
    else:
        return HttpResponse('Error! Missing parameters! [area_number, ard_mac, command] this three parameters is needed!')


# 用户注册（权限：所有人）
class UserRegister(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    permission_classes = (permissions.AllowAny,)


# 用户登录（权限：所有人）
class UserLogin(APIView):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        try:
            user = User.objects.get(username__exact=username)
        except User.DoesNotExist:
            return Response('username error', HTTP_400_BAD_REQUEST)
        if user.check_password(password):
            serializer = UserLoginSerializer(user)
            new_data = serializer.data
            # 记忆已登录用户
            self.request.session['user_id'] = user.id
            return Response(new_data, status=HTTP_200_OK)
        return Response('password error', HTTP_400_BAD_REQUEST)


# 用户登出
def user_logout(request):
    logout(request)
    return HttpResponse('logout success!')


# 显示所有用户列表（权限：管理员）
class UserList(generics.ListAPIView):
    """
    Permissions: Only administrators have permission to read the userlist.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # permission_classes = (permissions.IsAdminUser,)


# 获取、更新或删除某个用户实例（权限：管理员）
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Permissions: Only administrators have permission to Retrieve, update or delete the user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # permission_classes = (permissions.IsAdminUser,)


# 显示所有大棚(区域)列表(权限：管理员)
class AreaList(generics.ListAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer

    # permission_classes = (permissions.IsAdminUser,)


# 创建一个新大棚
class AreaCreate(generics.CreateAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# 获得GET、更新PUT、删除DELETE某个大棚实例，(E.g. /areas/1/ :获取、更新或删除大棚编号为1的实例)
class AreaDetail(APIView):

    def get_object(self, pk):
        try:
            return Area.objects.get(number=pk)
        except Area.DoesNotExist:
            return Http404

    # 获得某个大棚实例
    def get(self, request, pk, format=None):
        area = self.get_object(pk)
        serializer = AreaSerializer(area)
        return Response(serializer.data)

    # 修改某个大棚实例，并将修改后的阈值信息发送给树莓派
    def put(self, request, pk, format=None):
        area = self.get_object(pk)
        serializer = AreaSerializer(area, data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Server在【Device】中查找该大棚下所有的设备的MAC地址
            device_mac_list = Device.objects.values_list("Ard_mac").filter(Area_number=pk)

            # 如果该大棚下有设备存在的话:
            if device_mac_list.exists():
                # 取出修改完后的阈值信息
                temp_max = Area.objects.values("temp_max").filter(number=pk).first()['temp_max']
                temp_min = Area.objects.values("temp_min").filter(number=pk).first()['temp_min']
                temp_shake = Area.objects.values("temp_shake").filter(number=pk).first()['temp_shake']
                humidity_min = Area.objects.values("humidity_min").filter(number=pk).first()['humidity_min']
                humidity_shake = Area.objects.values("humidity_shake").filter(number=pk).first()['humidity_shake']
                light_min = Area.objects.values("light_min").filter(number=pk).first()['light_min']
                light_shake = Area.objects.values("light_shake").filter(number=pk).first()['light_shake']
                threshold = {
                    'temp_max': temp_max,
                    'temp_min': temp_min,
                    'temp_shake': temp_shake,
                    'humidity_min': humidity_min,
                    'humidity_shake': humidity_shake,
                    'light_min': light_min,
                    'light_shake': light_shake
                }
                json_threshold = json.dumps(threshold, ensure_ascii=False)

                for device_mac in device_mac_list:
                    # 获得设备的MAC地址
                    Ard_mac = device_mac[0]
                    # 根据该设备的MAC地址，在【数据】中查找这些节点的最新对应的树莓派IP
                    Rbp_ip = Agri.objects.values_list("Rbp_ip").filter(Ard_mac=Ard_mac).first()[0]
                    # 将阈值信息通过UDP发送给树莓派
                    serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    serversocket.sendto(json_threshold.encode('utf-8'), (Rbp_ip, 7777))

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 删除某个大棚实例
    def delete(self, request, pk, format=None):
        area = self.get_object(pk)
        area.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 显示某用户的所有大棚（区域）列表（权限：认证的用户）（E.g. /arealist/1/    :显示id为1的用户的所有大棚（区域）列表）
class SpecificAreaList(APIView):
    @staticmethod
    def get_object(pk):
        try:
            return Area.objects.filter(owner=pk)
        except Area.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        Area_list = self.get_object(pk)
        serializer = AreaSerializer(Area_list, many=True)
        return Response(serializer.data)


# 创建一个新大棚（区域）及其设备
class AreaDeviceCreate(APIView):

    def post(self, request, format=None):
        # request.body.decode()的结果是一个json字符串，调用json.loads()转为Python字典，然后获取对应值
        req = json.loads(request.body.decode())
        # 获取【Area】中最新的一条数据的number值
        result = Area.objects.all()
        if result.count() == 0:
            number = 0
        else:
            number_last = Area.objects.values("number").order_by('-number').first()['number']
            number = number_last + 1
        name = req['name']
        longitude = str(req['longitude'])
        latitude = str(req['latitude'])
        crops = req['plant']
        status = req.get('status', '正常')
        detail = req.get('detail', '无')
        user_id = request.session['user_id']
        # 在【user】中查找该user_id的用户实例
        owner = User.objects.get(id=user_id)
        temp_max = req.get('temp_max', '26')
        temp_min = req.get('temp_min', '20')
        temp_shake = req.get('temp_shake', '1')
        humidity_min = req.get('humidity_min', '0')
        humidity_shake = req.get('humidity_shake', '1')
        light_min = req.get('light_min', '100')
        light_shake = req.get('light_shake', '80')

        # 将数据存储进【Area】
        Area.objects.create(number=number, name=name, longitude=longitude, latitude=latitude, crops=crops,
                            status=status, detail=detail, owner=owner,
                            temp_max=temp_max, temp_min=temp_min, temp_shake=temp_shake, humidity_min=humidity_min,
                            humidity_shake=humidity_shake, light_min=light_min, light_shake=light_shake)

        # 新建该大棚所属设备
        distribution = req['distribution']
        for device in distribution:
            Ard_mac = device['mac']
            kind = device.get('kind', '未知')
            x = str(device['x'])
            y = str(device['y'])
            Area_number = Area.objects.get(number=number)
            # 将数据存储进【Device】
            Device.objects.create(Ard_mac=Ard_mac, kind=kind, x=x, y=y, Area_number=Area_number)

        response = HttpResponse('Success!')
        response['Access-Control-Expose-Headers'] = 'sessionid'
        return response


# 获得一个大棚（区域）实例及其设备
class AreaDeviceDetailGet(APIView):
    # 获取大棚实例函数
    def get_object_area(self, pk):
        try:
            return Area.objects.get(number=pk)
        except Area.DoesNotExist:
            raise Http404

    # 获取编号为pk的大棚及其设备，转为json格式返回
    def get(self, request, pk, format=None):
        area = self.get_object_area(pk)
        name = area.name
        plant = area.crops
        longitude = float(area.longitude)
        latitude = float(area.latitude)
        distribution = []
        # 在【Device】中查找该大棚下所有的节点
        device_list = Device.objects.values_list("x", "y", "Ard_mac").filter(Area_number=pk)
        for device in device_list:
            x = float(device[0])
            y = float(device[1])
            mac = device[2]
            device_data = {
                'x': x,
                'y': y,
                'mac': mac
            }
            distribution.append(device_data)

        response = {
            'number': pk,
            'name': name,
            'plant': plant,
            'longitude': longitude,
            'latitude': latitude,
            'distribution': distribution
        }
        response_json = json.dumps(response, ensure_ascii=False)
        return HttpResponse(response_json)


# 修改大棚信息以及该大棚下的设备(E.g. /areas-devices-modify/1/ :修改大棚编号为1的实例及该大棚下的设备)
class AreaDeviceDetailModify(APIView):
    def post(self, request, pk, format=None):
        # request.body.decode()的结果是一个json字符串，调用json.loads()转为Python字典，然后获取对应值
        req = json.loads(request.body.decode())
        number = pk
        name = req['name']
        longitude = str(req['longitude'])
        latitude = str(req['latitude'])
        crops = req['plant']
        status = req.get('status', '正常')
        detail = req.get('detail', '无')
        user_id = request.session['user_id']
        # 在【user】中查找该user_id的用户实例
        owner = User.objects.get(id=user_id)
        temp_max = req.get('temp_max', '26')
        temp_min = req.get('temp_min', '20')
        temp_shake = req.get('temp_shake', '1')
        humidity_min = req.get('humidity_min', '0')
        humidity_shake = req.get('humidity_shake', '1')
        light_min = req.get('light_min', '100')
        light_shake = req.get('light_shake', '80')

        # 在【Area】中修改编号为number的大棚数据
        Area.objects.filter(number=number).update(name=name, longitude=longitude, latitude=latitude,
                                                  crops=crops, status=status, detail=detail, owner=owner,
                                                  temp_max=temp_max, temp_min=temp_min, temp_shake=temp_shake,
                                                  humidity_min=humidity_min, humidity_shake=humidity_shake,
                                                  light_min=light_min, light_shake=light_shake)

        # 在【Device】中删除编号为number的大棚下的所有节点
        Device.objects.filter(Area_number=number).delete()

        # 新建该大棚所属设备
        distribution = req['distribution']
        for device in distribution:
            Ard_mac = device['mac']
            kind = device.get('kind', '未知')
            x = str(device['x'])
            y = str(device['y'])
            Area_number = Area.objects.get(number=number)
            # 将数据存储进【Device】
            Device.objects.create(Ard_mac=Ard_mac, kind=kind, x=x, y=y, Area_number=Area_number)

        return HttpResponse('Success!')


# 获取某大棚详情信息：其中包括大棚信息、及其设备信息、以及每个设备的最新的一条传感器数据、设备控制的数据、报警记录数据（pk指代大棚编号）
class AreaDeviceDetailShow(APIView):
    # 获取大棚实例函数
    def get_object_area(self, pk):
        try:
            return Area.objects.get(number=pk)
        except Area.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        area = self.get_object_area(pk)
        name = area.name
        plant = area.crops
        longitude = float(area.longitude)
        latitude = float(area.latitude)
        distribution = []

        # 在【Device】中查找该大棚下所有的节点
        device_list = Device.objects.values_list("x", "y", "Ard_mac").filter(Area_number=pk)
        for device in device_list:
            x = float(device[0])
            y = float(device[1])
            # 取出设备的MAC地址
            mac = device[2]

            # 根据取出的设备MAC地址，在【Agri】中查找该设备下最新的一条传感器数据
            sensor_tuple = Agri.objects.values_list("soil_Humidity", "soil_Temp", "soil_Salinity",
                                                    "soil_EC", "air_Humidity","air_Temp",
                                                    "CO2_Concentration", "light_Intensity", "soil_PH",
                                                    "air_Pressure", "wind_Speed",
                                                    "O2_Concentration").filter(Ard_mac=mac).first()
            # 判断记录是否存在
            if sensor_tuple:
                soil_Humidity = sensor_tuple[0]
                soil_Temp = sensor_tuple[1]
                soil_Salinity = sensor_tuple[2]
                soil_EC = sensor_tuple[3]
                air_Humidity = sensor_tuple[4]
                air_Temp = sensor_tuple[5]
                CO2_Concentration = sensor_tuple[6]
                light_Intensity = sensor_tuple[7]
                soil_PH = sensor_tuple[8]
                air_Pressure = sensor_tuple[9]
                wind_Speed = sensor_tuple[10]
                O2_Concentration = sensor_tuple[11]
            else:
                soil_Humidity = '暂未有数据'
                soil_Temp = '暂未有数据'
                soil_Salinity = '暂未有数据'
                soil_EC = '暂未有数据'
                air_Humidity = '暂未有数据'
                air_Temp = '暂未有数据'
                CO2_Concentration = '暂未有数据'
                light_Intensity = '暂未有数据'
                soil_PH = '暂未有数据'
                air_Pressure = '暂未有数据'
                wind_Speed = '暂未有数据'
                O2_Concentration = '暂未有数据'

            # 根据取出的设备MAC地址，在【Control】中查找该设备下最新的一条设备控制数据
            control_tuple = Control.objects.values_list("light_control", "temp_control", "waterPump_control",
                                                        "fan_control").filter(Ard_mac=mac).order_by("-created").first()

            # 判断记录是否存在
            if control_tuple:
                light_control = control_tuple[0]
                temp_control = control_tuple[1]
                waterPump_control = control_tuple[2]
                fan_control = control_tuple[3]
            else:
                # 约定-999代表暂未有数据
                light_control = -999
                temp_control = -999
                waterPump_control = -999
                fan_control = -999

            # 根据取出的设备MAC地址，在【Alarm】中查找该设备下最新的一条报警记录数据
            alarm_tuple = Alarm.objects.values_list("content").filter(Ard_mac=mac).order_by("-created").first()

            # 判断记录是否存在
            if alarm_tuple:
                content = alarm_tuple[0]
            else:
                content = '暂未有数据'

            # 将每个设备所取得的数据以list形式都存在distribution中
            device_data = {
                'x': x,
                'y': y,
                'mac': mac,
                'soil_Humidity': soil_Humidity,
                'soil_Temp': soil_Temp,
                'soil_Salinity': soil_Salinity,
                'soil_EC': soil_EC,
                'air_Humidity': air_Humidity,
                'air_Temp': air_Temp,
                'CO2_Concentration': CO2_Concentration,
                'light_Intensity': light_Intensity,
                'soil_PH': soil_PH,
                'air_Pressure': air_Pressure,
                'wind_Speed': wind_Speed,
                'O2_Concentration': O2_Concentration,
                'light_control': light_control,
                'temp_control': temp_control,
                'waterPump_control': waterPump_control,
                'fan_control': fan_control,
                'content': content
            }
            distribution.append(device_data)

        response = {
            'number': pk,
            'name': name,
            'plant': plant,
            'longitude': longitude,
            'latitude': latitude,
            'distribution': distribution
        }

        response_json = json.dumps(response, ensure_ascii=False)
        return HttpResponse(response_json)


# 获取当前用户的大棚数量、arduino数量、报警记录的数量
class AreaDeviceAlarmCount(APIView):
    def get(self, request, pk, format=None):
        # 获取当前用户的大棚列表以及大棚数量
        owner = User.objects.get(id=pk)
        areas_list = Area.objects.filter(owner=owner)
        areas_count = areas_list.count()

        devices_count = 0
        alarms_count = 0
        # 根据获取的大棚列表，得到arduino数量和报警记录数量
        for area in areas_list:
            devices_count += Device.objects.filter(Area_number=area.number).count()
            content_blank_count = Alarm.objects.filter(Area_number=area.number, content='').count()
            alarms_total = Alarm.objects.filter(Area_number=area.number).count()
            alarms_count = alarms_total - content_blank_count

        data = {
            'areas_count': areas_count,
            'devices_count': devices_count,
            'alarms_count': alarms_count
        }
        data_json = json.dumps(data, ensure_ascii=False)

        return HttpResponse(data_json)


# # 显示所有Arduino类型列表/创建一个新Arduino类型（权限：认证的用户）
# class KindOfArduinoList(generics.ListCreateAPIView):
#     queryset = KindOfArduino.objects.all()
#     serializer_class = KindOfArduinoSerializer
#
#     # permission_classes = (permissions.IsAuthenticated,)


# 显示所有设备列表（权限：管理员）
class DeviceList(generics.ListAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    # permission_classes = (permissions.IsAdminUser,)


# 新建一个设备（权限：认证的用户）
class DeviceCreate(generics.CreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    # permission_classes = (permissions.IsAuthenticated,)


# 获得、更新、删除一个设备实例（权限：认证的用户）(E.g. /devices/ardmac111/ :获取、更新或删除Ard_mac地址为ardmac111的实例)
class DeviceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    # permission_classes = (permissions.IsAuthenticated,)


# 显示某大棚下的所有设备列表（权限：认证的用户）（E.g. /devicelist/1/    :显示id为1的大棚下的所有设备列表）
class SpecificDeviceList(APIView):
    @staticmethod
    def get_object(pk):
        try:
            return Device.objects.filter(Area_number=pk)
        except Device.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        Device_list = self.get_object(pk)
        serializer = DeviceSerializer(Device_list, many=True)
        return Response(serializer.data)

    # permission_classes = (permissions.IsAuthenticated,)


# 显示所有iot数据列表(权限：管理员)
class AgriList(generics.ListAPIView):
    queryset = Agri.objects.all()
    serializer_class = AgriSerializer

    # permission_classes = (permissions.IsAdminUser,)


# 传感器数据与控制设备开关数据的接收与阈值返回
def AgriCreate(request):
    """
    1. 每次接收来自树莓派的数据时，将传感器数据以及树莓派的IP存储到【数据】中，将设备的控制开关数据存储到【Control】中
    2. 在【Device】中查找传过来的数据中Arduino_MAC对应的大棚编号
    3. 根据大棚编号在【Area】中找到该大棚的所有阈值信息
    4. 将阈值信息通过UDP发送给树莓派
    """
    global info
    Rbp_ip = request.META['REMOTE_ADDR']
    if request.method == 'POST':
        # request.body.decode()的结果是一个json字符串，调用json.loads()转为Python字典，然后获取对应值
        req = json.loads(request.body.decode())
        try:
            info = 'Send successfully!'

            Rbp_mac = req['Rbp_mac']
            Ard_mac = req['Ard_mac']
            kind = req['kind']
            soil_Humidity = req['soil_Humidity']
            soil_Temp = req['soil_Temp']
            soil_Salinity = req['soil_Salinity']
            soil_EC = req['soil_EC']
            air_Humidity = req['air_Humidity']
            air_Temp = req['air_Temp']
            CO2_Concentration = req['CO2_Concentration']
            light_Intensity = req['light_Intensity']
            soil_PH = req['soil_PH']
            air_Pressure = req['air_Pressure']
            wind_Speed = req['wind_Speed']
            O2_Concentration = req['O2_Concentration']
            created = req['created']
            light_control = req['light_control']
            temp_control = req['temp_control']
            waterPump_control = req['waterPump_control']
            fan_control = req['fan_control']

            # 在【Device】中查找该Arduino_MAC对应的大棚编号
            Area_number = Device.objects.values("Area_number").filter(Ard_mac=Ard_mac).first()['Area_number']

            # 每次接收来自树莓派的数据时，将数据以及树莓派的IP存储到【数据】中,其中Ard_mac为外键，需预处理
            device1 = Device.objects.get(Ard_mac=Ard_mac)
            Agri.objects.create(Rbp_mac=Rbp_mac, Ard_mac=device1, Rbp_ip=Rbp_ip, Area_number=Area_number,
                                kind=kind,soil_Humidity=soil_Humidity, soil_Temp=soil_Temp,
                                soil_Salinity=soil_Salinity, soil_EC=soil_EC, air_Humidity=air_Humidity,
                                air_Temp=air_Temp, CO2_Concentration=CO2_Concentration,
                                light_Intensity=light_Intensity, soil_PH=soil_PH, air_Pressure=air_Pressure,
                                wind_Speed=wind_Speed, O2_Concentration=O2_Concentration, created=created)

            # 每次接收来自树莓派的数据时，将数据中有关设备的控制开关的部分存储到【Control】中
            Control.objects.create(Ard_mac=Ard_mac, light_control=light_control, temp_control=temp_control,
                                   waterPump_control=waterPump_control, fan_control=fan_control, created=created)

            # 根据大棚编号在【Area】中找到该大棚的所有阈值信息
            temp_max = Area.objects.values("temp_max").filter(number=Area_number).first()['temp_max']
            temp_min = Area.objects.values("temp_min").filter(number=Area_number).first()['temp_min']
            temp_shake = Area.objects.values("temp_shake").filter(number=Area_number).first()['temp_shake']
            humidity_min = Area.objects.values("humidity_min").filter(number=Area_number).first()['humidity_min']
            humidity_shake = Area.objects.values("humidity_shake").filter(number=Area_number).first()['humidity_shake']
            light_min = Area.objects.values("light_min").filter(number=Area_number).first()['light_min']
            light_shake = Area.objects.values("light_shake").filter(number=Area_number).first()['light_shake']
            threshold = {
                'temp_max': temp_max,
                'temp_min': temp_min,
                'temp_shake': temp_shake,
                'humidity_min': humidity_min,
                'humidity_shake': humidity_shake,
                'light_min': light_min,
                'light_shake': light_shake
            }
            json_threshold = json.dumps(threshold, ensure_ascii=False)

            # 将阈值信息通过UDP发送给树莓派
            serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            serversocket.sendto(json_threshold.encode('utf-8'), (Rbp_ip, 7777))

        except Exception:
            info = 'Iot and Control data send failed!'

        return HttpResponse(info)
    else:
        info = 'Request error!'
        # serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # serversocket.sendto(info.encode('utf-8'), (Rbp_ip, 7777))
        return HttpResponse(info)


# 获得、更新、删除一个iot数据实例（权限：认证的用户）
class AgriDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Agri.objects.all()
    serializer_class = AgriSerializer

    # permission_classes = (permissions.IsAuthenticated,)


# 显示某Arduino产生的所有iot数据列表（E.g. /agrilist/ardmac111/ :显示ard_mac为ardmac111的Arduino下的所有iot数据列表）
class SpecificAgriList(APIView):
    @staticmethod
    def get_object(pk):
        try:
            return Agri.objects.filter(Ard_mac=pk)
        except Agri.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        Agri_list = self.get_object(pk)
        serializer = AgriSerializer(Agri_list, many=True)
        return Response(serializer.data)

    # permission_classes = (permissions.IsAuthenticated,)


# 显示某Arduino所产生的最新的n条iot数据列表(权限：认证的用户)(E.g. /agrilist/1/1/:显示id为1的Arduino下的最新的一条iot数据列表）
class LimitAgriList(APIView):
    @staticmethod
    def get_object(pk, number):
        try:
            return Agri.objects.filter(Ard_mac=pk)[:number]
        except Agri.DoesNotExist:
            return Http404

    def get(self, request, pk, number, format=None):
        Agri_list = self.get_object(pk, number)
        serializer = AgriSerializer(Agri_list, many=True)
        return Response(serializer.data)


# 显示某大棚下所有iot数据列表
class SpecificAgriListArea(APIView):
    @staticmethod
    def get_object(pk):
        try:
            return Agri.objects.filter(Area_number=pk)
        except Agri.DoesNotExist:
            return Http404

    def get (self, request, pk, format=None):
        Agri_list = self.get_object(pk)
        serializer = AgriSerializer(Agri_list, many=True)
        return Response(serializer.data)


# 显示某大棚下所产生的最新的n条iot数据列表(E.g. /agrilist-area/1/1/ :显示大棚编号为1下最新的1条iot数据列表)
class LimitAgriListArea(APIView):
    @staticmethod
    def get_object(pk, number):
        try:
            return Agri.objects.filter(Area_number=pk).order_by('-created')[:number]
        except Agri.DoesNotExist:
            return Http404

    def get(self, request, pk, number, format=None):
        Agri_list = self.get_object(pk, number)
        serializer = AgriSerializer(Agri_list, many=True)
        return Response(serializer.data)


# 显示所有报警记录列表
class AlarmList(generics.ListAPIView):
    queryset = Alarm.objects.all()
    serializer_class = AlarmSerializer


# 接收来自树莓派的报警记录信息
def AlarmCreate(request):
    """
    1. 由树莓派发送给Server报警记录的数据，[树莓派_mac、Arduino_mac、产生时间、内容]
    2. Server在【Device】中查找该Ard_mac对应的大棚编号
    3. 得到 [大棚编号、树莓派_mac、Ard_mac、产生时间、内容]
    4. 在【Alarm】中取出该Ard_mac下最新的一条数据，判断是否存在
    5. 如果存在，则将此次收到的Area_number+content与取出的数据的Area_number+content进行比对。
        1）如果相同，则将取出的数据的结束时间赋值为-999
        2）如果不同，则将此次接收到的数据的产生时间赋值给取出的数据的结束时间并更新该条数据, 然后将此次将此次接收到的数据存进【Alarm】中，其中结束时间等于-999
    6. 如果不存在，则将这次收到的数据 [大棚编号、树莓派_mac、Ard_mac、产生时间、内容]存进【Alarm】，其中结束时间为-999
    7. 每当收到一条报警记录且其content不为空，则将该报警记录所在大棚的状态置为警告
    8. 若content的内容为空，查询此大棚下所有节点的最新的一条报警记录，若其content都为空，则将大棚的状态置为正常
    """
    # 提示信息
    global info
    # 获取发送端的IP地址
    Rbp_ip = request.META['REMOTE_ADDR']
    if request.method == 'POST':
        # request.body.decode()的结果是一个json字符串，调用json.loads()转为Python字典，然后获取对应值
        req = json.loads(request.body.decode())
        try:
            info = 'Alarm send successfully!'
            Rbp_mac = req['Rbp_mac']
            Ard_mac = req['Ard_mac']
            created = req['created']
            content = req['content']

            # 在【Device】中查找该Arduino_mac对应的大棚编号
            Area_number = Device.objects.values("Area_number").filter(Ard_mac=Ard_mac).first()['Area_number']

            # 在【Alarm】中取出该Ard_mac下最新的一条数据，判断是否存在
            alarm_last = Alarm.objects.filter(Ard_mac=Ard_mac).order_by('-created').first()
            if alarm_last:
                # 将此次收到的Area_number + content与取出的数据的Area_number + content进行比对。
                if alarm_last.Area_number == Area_number and alarm_last.content == content:
                    # 如果相同，则将取出的数据的结束时间赋值为 - 999
                    alarm_last.end_time = -999
                    alarm_last.Rbp_mac = Rbp_mac
                    alarm_last.save()
                else:
                    # 如果不同，则将此次接收到的数据的产生时间赋值给取出的数据的结束时间并更新该条数据
                    alarm_last.end_time = created
                    alarm_last.save()
                    # 然后将此次接收到的数据存进【Alarm】中，其中结束时间等于-999
                    Alarm.objects.create(Area_number=Area_number, Rbp_mac=Rbp_mac, Ard_mac=Ard_mac,
                                         created=created, content=content, end_time=-999)

            # 如果不存在，则将这次收到的数据 [大棚编号、树莓派_mac、Ard_mac、产生时间、内容]存进【Alarm】，其中结束时间为-999
            else:
                Alarm.objects.create(Area_number=Area_number, Rbp_mac=Rbp_mac, Ard_mac=Ard_mac,
                                     created=created, content=content, end_time=-999)

            # 判断收到的报警记录的content是否为空
            # 若content不为空，则将该报警记录所在大棚的状态置为警告
            if content != '':
                Area.objects.filter(number=Area_number).update(status='警告')

            # 若content的内容为空，查询此大棚下所有节点的最新的一条报警记录，若其content都为空，则将大棚的状态置为正常
            else:
                ard_mac_list = Device.objects.values_list("Ard_mac").filter(Area_number=Area_number)
                flag = ''
                if ard_mac_list.exists():
                    for ard_mac in ard_mac_list:
                        Ard_mac = ard_mac[0]
                        # 根据得到的Ard_mac，在【Alarm】中查找最新的一条记录的内容
                        content_last = Alarm.objects.values_list("content").filter(Ard_mac=Ard_mac).order_by('-created').first()[0]
                        if content_last != '':
                            flag = '警告'
                            break

                    if flag == '':
                        Area.objects.filter(number=Area_number).update(status='正常')

        except Exception:
            info = 'Alarm send failed!'
        return HttpResponse(info)
    else:
        info = 'Request error!'
        return HttpResponse(info)


# 获得GET、更新PUT、删除DELETE某个报警记录实例，(E.g. /alarms/1/ :获取、更新或删除报警记录id为1的实例)
class AlarmDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Alarm.objects.all()
    serializer_class = AlarmSerializer


# 显示某大棚下的所有报警记录列表（E.g. /alarmlist/1/    :显示大棚编号为1的大棚下的所有报警记录列表）
class SpecificAlarmList(APIView):
    @staticmethod
    def get_object(pk):
        try:
            return Alarm.objects.filter(Area_number=pk)
        except Alarm.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        Alarm_list = self.get_object(pk)
        serializer = AlarmSerializer(Alarm_list, many=True)
        return Response(serializer.data)


# 显示某大棚下的所有的最新的n条报警记录列表(E.g. /alarmlist/1/1/:显示大棚编号为1的大棚下的最新的1条报警记录列表）
class LimitAlarmList(APIView):
    @staticmethod
    def get_object(pk, number):
        try:
            return Alarm.objects.filter(Area_number=pk).order_by('-created')[:number]
        except Alarm.DoesNotExist:
            return Http404

    def get(self, request, pk, number, format=None):
        Alarm_list = self.get_object(pk, number)
        serializer = AlarmSerializer(Alarm_list, many=True)
        return Response(serializer.data)


# 显示某Arduino下的所有报警记录列表（E.g. /alarmlist-ard/ardmac111/  :显示ard_mac为ardmac111的arduino下的所有报警记录列表）
class SpecificAlarmListArd(APIView):
    @staticmethod
    def get_object(pk):
        try:
            return Alarm.objects.filter(Ard_mac=pk)
        except Alarm.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        Alarm_list = self.get_object(pk)
        serializer = AlarmSerializer(Alarm_list, many=True)
        return Response(serializer.data)


# 显示某Arduino下的所有的最新的n条报警记录列表（E.g. /alarmlist-ard/ardmac111/1/ :显示ard_mac为ardmac111的arduino下的最新的1条报警记录列表）
class LimitAlarmListArd(APIView):
    @staticmethod
    def get_object(pk, number):
        try:
            return Alarm.objects.filter(Ard_mac=pk).order_by('-created')[:number]
        except Alarm.DoesNotExist:
            return Http404

    def get(self, request, pk, number, format=None):
        Alarm_list = self.get_object(pk, number)
        serializer = AlarmSerializer(Alarm_list, many=True)
        return Response(serializer.data)


# 显示某用户下所有的报警记录,其中包括大棚名称+Ard_MAC+报警内容+报警记录产生时间以及结束时间(其中pk代表用户id)
class SpecificAlarmListUser(APIView):
    def get(self, request, format=None):
        # 获得该用户下的大棚列表
        user_id = request.session['user_id']
        owner = User.objects.get(id=user_id)
        areas_list = Area.objects.filter(owner=owner)
        data = []
        for area in areas_list:
            Area_number = area.number
            Area_name = area.name
            # 获得该大棚编号下的报警记录列表
            alarms_list = Alarm.objects.filter(Area_number=Area_number)
            for alarm in alarms_list:
                Ard_mac = alarm.Ard_mac
                content = alarm.content
                if content == '':
                    continue
                created = alarm.created
                end_time = alarm.end_time
                temp = {
                    'Area_number': Area_number,
                    'Area_name': Area_name,
                    'Ard_mac': Ard_mac,
                    'content': content,
                    'created': created,
                    'end_time': end_time
                }
                data.append(temp)

        data_json = json.dumps(data, ensure_ascii=False)
        return HttpResponse(data_json)


# 查看某用户所有的大棚ID、名称以及各个大棚下Arduino的MAC地址(E.g. areas-devices-list/1/ : 显示用户id为1的用户所拥有的大棚列表及其设备列表)
class AreaDeviceList(APIView):
    def get(self, request, pk, format=None):
        data = []
        # 在【Area】获取该用户下的所有大棚的编号及名称列表
        area_list = Area.objects.values_list("number", "name").filter(owner=pk)

        # 获取所需数据
        for area in area_list:
            Area_number = area[0]
            name = area[1]
            # 在【Device】中获取当前编号下的大棚所拥有的所有设备MAC地址
            device_mac_list = Device.objects.values_list("Ard_mac").filter(Area_number=Area_number)
            list_temp = []
            for device_mac in device_mac_list:
                mac_dic = {
                    'mac': device_mac[0]
                }
                list_temp.append(mac_dic)

            dic_temp = {
                'id': Area_number,
                'name': name,
                'distribution': list_temp
            }
            data.append(dic_temp)
        data_json = json.dumps(data, ensure_ascii=False)

        return HttpResponse(data_json)


# 根据设备的MAC地址，获取某天的数据,pk为Arduino的MAC地址，timestamp为当天的时间戳
class HistoryIoT(APIView):
    @staticmethod
    def get_object(pk, timestamp):
        try:
            start = timestamp
            end = timestamp + 86216
            return Agri.objects.filter(Ard_mac=pk).filter(created__range=(start, end))
        except Agri.DoesNotExist:
            return Http404

    def get(self, request, pk, timestamp, format=None):
        Agri_list = self.get_object(pk, timestamp)
        serializer = AgriSerializer(Agri_list, many=True)
        return Response(serializer.data)
