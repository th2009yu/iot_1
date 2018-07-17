from django.shortcuts import render
from rest_framework.views import APIView
# from .models import agri
# from .serializers import agriSerializer
from .models import Owner
from .models import Area
from .models import Field, Pond, Forest
from .serializers import OwnerSerializer
from .serializers import AreaSerializer
from .serializers import FieldSerializer, PondSerializer, ForestSerializer
from rest_framework.response import Response
from rest_framework import status, generics
from django.http import Http404
from django.http import HttpResponse
import socket, threading, time


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


# 显示所有大棚列表/创建一个新大棚
# class OwnerList(APIView):
#     """
#     list all Owners, or create a new Owner
#     """
#     def get(self, request, format=None):
#         Owner_list = Owner.objects.all()
#         serializer = OwnerSerializer(Owner_list, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = OwnerSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class OwnerList(generics.ListCreateAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


# 显示所有大棚列表/创建一个新大棚
# class AreaList(APIView):
#     """
#     list all Areas, or create a new Area
#     """
#     def get(self, request, format=None):
#         Area_list = Area.objects.all()
#         serializer = AreaSerializer(Area_list, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = AreaSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class AreaList(generics.ListCreateAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer


# 显示某用户的所有大棚列表（E.g. /arealist/aaa/    :显示aaa用户的所有大棚列表）
class SpecificAreaList(APIView):
    def get_object(self, name):
        try:
            return Area.objects.filter(owner=name)
        except Area.DoesNotExist:
            return Http404

    def get(self, request, name, format=None):
        Area_list = self.get_object(name)
        serializer = AreaSerializer(Area_list, many=True)
        return Response(serializer.data)


# 显示所有田野的所有数据列表/创建一个新田野
class FieldList(generics.ListCreateAPIView):
    queryset = Field.objects.all().order_by('number', '-created')
    serializer_class = FieldSerializer


# 查询某田野大棚的所有数据列表,按数据创建时间顺序排序（E.g. /field/1/     : 田野一号大棚的所有数据）
class SpecificFieldList(APIView):
    """
    list  all data of X number of Field
    """
    def get_object(self, number):
        try:
            return Field.objects.filter(number=number).order_by('-created')
        except Field.DoesNotExist:
            return Http404

    def get(self, request, number, format=None):
        Field_list = self.get_object(number)
        serializer = FieldSerializer(Field_list, many=True)
        return Response(serializer.data)

    # def post(self, request, format=None):
    #     serializer = FieldSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 查询某田野大棚的一定长度的数据列表,按数据创建时间顺序排序 （E.g. /field/1/100/     : 田野一号大棚的100条数据）
class SpecificLimitFieldList(APIView):
    """
    list given numbers of data of X number of Field
    """
    def get_object(self, number, length):
        try:
            return Field.objects.filter(number=number).order_by('-created')[:length]
        except Field.DoesNotExist:
            return Http404

    def get(self, request, number, length, format=None):
        Field_list = self.get_object(number, length)
        serializer = FieldSerializer(Field_list, many=True)
        return Response(serializer.data)


# 显示所有池塘的所有数据列表/创建一个新池塘
class PondList(generics.ListCreateAPIView):
    queryset = Pond.objects.all().order_by('number', '-created')
    serializer_class = PondSerializer


# 查询某池塘大棚的所有数据列表,按数据创建时间顺序排序（E.g. /pond/1/     : 池塘一号大棚的所有数据）
class SpecificPondList(APIView):
    """
    list  all data of X number of Pond
    """
    def get_object(self, number):
        try:
            return Pond.objects.filter(number=number).order_by('-created')
        except Pond.DoesNotExist:
            return Http404

    def get(self, request, number, format=None):
        Pond_list = self.get_object(number)
        serializer = PondSerializer(Pond_list, many=True)
        return Response(serializer.data)


# 查询某池塘大棚的一定长度的数据列表,按数据创建时间顺序排序 （E.g. /pond/1/100/     : 池塘一号大棚的100条数据）
class SpecificLimitPondList(APIView):
    """
    list given numbers of data of X number of Pond
    """
    def get_object(self, number, length):
        try:
            return Pond.objects.filter(number=number).order_by('-created')[:length]
        except Pond.DoesNotExist:
            return Http404

    def get(self, request, number, length, format=None):
        Pond_list = self.get_object(number, length)
        serializer = PondSerializer(Pond_list, many=True)
        return Response(serializer.data)


# 显示所有森林的所有数据列表/创建一个新森林
class ForestList(generics.ListCreateAPIView):
    queryset = Forest.objects.all().order_by('number', '-created')
    serializer_class = ForestSerializer


# 查询某森林大棚的所有数据列表,按数据创建时间顺序排序（E.g. /forest/1/     : 森林一号大棚的所有数据）
class SpecificForestList(APIView):
    """
    list  all data of X number of Forest
    """
    def get_object(self, number):
        try:
            return Forest.objects.filter(number=number).order_by('-created')
        except Forest.DoesNotExist:
            return Http404

    def get(self, request, number, format=None):
        Forest_list = self.get_object(number)
        serializer = ForestSerializer(Forest_list, many=True)
        return Response(serializer.data)


# 查询某森林大棚的一定长度的数据列表,按数据创建时间顺序排序 （E.g. /forest/1/100/     : 池塘一号大棚的100条数据）
class SpecificLimitForestList(APIView):
    """
    list given numbers of data of X number of Forest
    """
    def get_object(self, number, length):
        try:
            return Forest.objects.filter(number=number).order_by('-created')[:length]
        except Forest.DoesNotExist:
            return Http404

    def get(self, request, number, length, format=None):
        Forest_list = self.get_object(number, length)
        serializer = ForestSerializer(Forest_list, many=True)
        return Response(serializer.data)


