from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from rest_framework.views import APIView
from IoT.permissions import *
from django.contrib.auth.models import User
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework import permissions
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.http import Http404
from django.http import HttpResponse
import socket
import time


# 客户端命令接口
def order(request):
    """
    receive command from client and send it to the cloud platform
    :return: command received from client
    """
    if request.GET.get('command'):
        command = request.GET['command']
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serversocket.sendto(b'ep=23SSMC3PDDQ7T1N7&pw=845962', ('115.29.240.46', 6000))
        time.sleep(1)
        serversocket.sendto(command.encode('utf-8'), ('115.29.240.46', 6000))
        return HttpResponse('send success!')
    else:
        return HttpResponse('send failed!')


# 用户注册
class UserRegister(APIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    @csrf_protect
    def post(self, request, format=None):
        data = request.data
        username = data.get('username')
        if User.objects.filter(username__exact=username):
            return Response("用户名已存在", HTTP_400_BAD_REQUEST)
        serializer = UserRegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


# List all owners
class UserList(generics.ListAPIView):
    """
    Permissions: Only administrators have permission to read the userlist.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = (permissions.IsAdminUser,)


# Create a new owner
class UserCreate(generics.CreateAPIView):
    """
    Permissions: Only administrators have permission to create a new owner.
    """
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    permission_classes = (permissions.IsAdminUser,)


# Retrieve, update or delete a owner instance.
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Permissions: Only administrators have permission to Retrieve, update or delete the user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = (permissions.IsAdminUser,)


# 显示所有大棚(区域)列表(权限：管理员)
class AreaList(generics.ListAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer

    permission_classes = (permissions.IsAdminUser,)


# 创建一个新大棚（区域）（权限：认证的用户）
class AreaCreate(generics.CreateAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    permission_classes = (permissions.IsAuthenticated,)


# 获得、更新、删除一个大棚（区域）实例（权限：管理者或者大棚拥有者）
class AreaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer

    permission_classes = (IsOwnerOrIsAdminUser,)


# 显示某用户的所有大棚（区域）列表（权限：认证的用户）（E.g. /areas_owner/1/    :显示id为1的用户的所有大棚（区域）列表）
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

    # 权限：认证的用户即可访问（应该是管理员及该用户本身，待改）
    permission_classes = (permissions.IsAuthenticated,)


# 显示所有Arduino类型列表/创建一个新Arduino类型（权限：认证的用户）
class KindOfArduinoList(generics.ListCreateAPIView):
    queryset = KindOfArduino.objects.all()
    serializer_class = KindOfArduinoSerializer

    permission_classes = (permissions.IsAuthenticated,)


# 显示所有设备列表/新建一个设备
class DeviceList(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


# 获得、更新、删除一个设备实例
class DeviceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


# 显示某大棚下的所有设备列表（E.g. /devicelist/1/    :显示id为1的大棚下的所有设备列表）
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


# 显示所有iot数据列表/新建一个新iot数据
class AgriList(generics.ListCreateAPIView):
    queryset = Agri.objects.all()
    serializer_class = AgriSerializer


# 获得、更新、删除一个iot数据实例
class AgriDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Agri.objects.all()
    serializer_class = AgriSerializer


# 显示某Arduino产生的所有iot数据列表（E.g. /agrilist/1/    :显示id为1的Arduino下的所有iot数据列表）
class SpecificAgriList(APIView):
    @staticmethod
    def get_object(pk):
        try:
            return Agri.objects.filter(Ard_number=pk)
        except Agri.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        Agri_list = self.get_object(pk)
        serializer = AgriSerializer(Agri_list, many=True)
        return Response(serializer.data)


# 显示某Arduino所产生的最新的n条iot数据列表（E.g. /agrilist/1/1/    :显示id为1的Arduino下的最新的一条iot数据列表）
class LimitAgriList(APIView):
    @staticmethod
    def get_object(pk, number):
        try:
            return Agri.objects.filter(Ard_number=pk)[:number]
        except Agri.DoesNotExist:
            return Http404

    def get(self, request, pk, number, format=None):
        Agri_list = self.get_object(pk, number)
        serializer = AgriSerializer(Agri_list, many=True)
        return Response(serializer.data)


# # 显示所有树莓派列表/创建一个新树莓派节点
# class RaspberryPiList(generics.ListCreateAPIView):
#     queryset = RaspberryPi.objects.all()
#     serializer_class = RaspberryPiSerializer
#
#
# # 显示某大棚（区域）内的所有树莓派列表（E.g. /rbplist/1/    :显示编号为1的大棚（区域）内所有的树莓派列表）
# class SpecificRaspberryPiList(APIView):
#     @staticmethod
#     def get_object(number):
#         try:
#             return RaspberryPi.objects.filter(belongTo=number)
#         except RaspberryPi.DoesNotExist:
#             return Http404
#
#     def get(self, request, number, format=None):
#         RaspberryPi_list = self.get_object(number)
#         serializer = RaspberryPiSerializer(RaspberryPi_list, many=True)
#         return Response(serializer.data)
#
#

#
#
# # 显示所有Arduino列表/创建一个新Arduino设备
# class ArduinoList(generics.ListCreateAPIView):
#     queryset = Arduino.objects.values('belongToArea', 'belongToRbp', 'number', 'kind')
#     serializer_class = ArduinoSerializer
#
#
# # 显示某大棚（区域）下的所有Arduino设备列表
# # (E.g. /areaofardlist/1/ :显示编号为1的大棚（区域）内所有的Arduino设备）
# class SpecificAreaArduinoList(APIView):
#     @staticmethod
#     def get_object(number_area):
#         try:
#             return Arduino.objects.filter(belongToArea=number_area)
#         except RaspberryPi.DoesNotExist:
#             return Http404
#
#     def get(self, request, number_area, format=None):
#         Arduino_list = self.get_object(number_area)
#         serializer = ArduinoSerializer(Arduino_list, many=True)
#         return Response(serializer.data)
#
#
# # 显示某个树莓派下的所有Arduino设备列表
# # (E.g. /rbpofardlist/1/ :显示编号为1的树莓派下的所有的Arduino设备）
# class SpecificRbpArduinoList(APIView):
#     @staticmethod
#     def get_object(number_rbp):
#         try:
#             return Arduino.objects.filter(belongToRbp=number_rbp)
#         except Arduino.DoesNotExist:
#             return Http404
#
#     def get(self, request, number_rbp, format=None):
#         Arduino_list = self.get_object(number_rbp)
#         serializer = ArduinoSerializer(Arduino_list, many=True)
#         return Response(serializer.data)
#
#
# # 显示所有iot数据列表/创建一个新的iot数据
# class AgriList(generics.ListCreateAPIView):
#     queryset = Agri.objects.all()
#     serializer_class = AgriSerializer
#
#
# # 显示某大棚（区域）里所有的iot数据列表
# # (E.g. /areaofagrilist/1/ :显示编号为1的大棚（区域）下所有的iot数据）
# class SpecificAreaAgriList(APIView):
#     @staticmethod
#     def get_object(number_area):
#         try:
#             return Agri.objects.filter(belongToArea=number_area)
#         except Agri.DoesNotExist:
#             return Http404
#
#     def get(self, request, number_area, format=None):
#         Agri_list = self.get_object(number_area)
#         serializer = AgriSerializer(Agri_list, many=True)
#         return Response(serializer.data)
#
#
# # 显示某树莓派下所有的iot数据列表
# # (E.g. /rbpofagrilist/1/ :显示编号为1的树莓派下所有的iot数据）
# class SpecificRbpAgriList(APIView):
#     @staticmethod
#     def get_object(number_rbp):
#         try:
#             return Agri.objects.filter(belongToRbp=number_rbp)
#         except Agri.DoesNotExist:
#             return Http404
#
#     def get(self, request, number_rbp, format=None):
#         Agri_list = self.get_object(number_rbp)
#         serializer = AgriSerializer(Agri_list, many=True)
#         return Response(serializer.data)
#
#
# # 显示某Arduino下所有的iot数据列表
# # (E.g. /ardofagrilist/1/ :显示编号为1的Arduino下所有的iot数据）
# class SpecificArdAgriList(APIView):
#     @staticmethod
#     def get_object(number_ard):
#         try:
#             return Agri.objects.filter(belongToArd=number_ard)
#         except Agri.DoesNotExist:
#             return Http404
#
#     def get(self, request, number_ard, format=None):
#         Agri_list = self.get_object(number_ard)
#         serializer = AgriSerializer(Agri_list, many=True)
#         return Response(serializer.data)
