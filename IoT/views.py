from rest_framework.views import APIView
from IoT.permissions import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework import permissions
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.http import Http404
from django.http import HttpResponse
import socket
import time
from django.contrib.auth import logout


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

    def post (self, request, format=None):
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

    permission_classes = (permissions.IsAdminUser,)


# # Create a new owner
# class UserCreate(generics.CreateAPIView):
#     """
#     Permissions: Only administrators have permission to create a new owner.
#     """
#     queryset = User.objects.all()
#     serializer_class = UserCreateSerializer
#
#     permission_classes = (permissions.IsAdminUser,)


# 获取、更新或删除某个用户实例（权限：管理员）
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

    # 权限：认证的用户即可访问（应该是管理员及该用户本身，待改）
    permission_classes = (permissions.IsAuthenticated,)


# 显示所有Arduino类型列表/创建一个新Arduino类型（权限：认证的用户）
class KindOfArduinoList(generics.ListCreateAPIView):
    queryset = KindOfArduino.objects.all()
    serializer_class = KindOfArduinoSerializer

    permission_classes = (permissions.IsAuthenticated,)


# 显示所有设备列表（权限：管理员）
class DeviceList(generics.ListAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    permission_classes = (permissions.IsAdminUser,)


# 新建一个设备（权限：认证的用户）
class DeviceCreate(generics.CreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    permission_classes = (permissions.IsAuthenticated,)


# 获得、更新、删除一个设备实例（权限：认证的用户）
class DeviceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    permission_classes = (permissions.IsAuthenticated,)


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

    permission_classes = (permissions.IsAuthenticated,)


# 显示所有iot数据列表(权限：管理员)
class AgriList(generics.CreateAPIView):
    queryset = Agri.objects.all()
    serializer_class = AgriSerializer

    permission_classes = (permissions.IsAdminUser,)


# 新建一个新iot数据(权限：认证的用户)
class AgriCreate(generics.CreateAPIView):
    queryset = Agri.objects.all()
    serializer_class = AgriSerializer

    permission_classes = (permissions.IsAuthenticated,)


# 获得、更新、删除一个iot数据实例（权限：认证的用户）
class AgriDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Agri.objects.all()
    serializer_class = AgriSerializer

    permission_classes = (permissions.IsAuthenticated,)


# 显示某Arduino产生的所有iot数据列表（权限：认证的用户）（E.g. /agrilist/1/    :显示id为1的Arduino下的所有iot数据列表）
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

    permission_classes = (permissions.IsAuthenticated,)


# 显示某Arduino所产生的最新的n条iot数据列表(权限：认证的用户)(E.g. /agrilist/1/1/:显示id为1的Arduino下的最新的一条iot数据列表）
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

    permission_classes = (permissions.IsAuthenticated,)
