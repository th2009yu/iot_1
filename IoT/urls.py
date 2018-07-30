from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    # 客户端命令接口
    path('order', views.order),

    # 用户注册
    path('users/register/', views.UserRegister.as_view()),
    # List all users
    path('users/all/', views.UserList.as_view()),
    # Create a new owner
    path('users/new/', views.UserCreate.as_view()),
    # Retrieve a user instance.（按照用户id索引）
    path('users/<int:pk>/', views.UserDetail.as_view()),

    # 显示所有大棚（区域）列表(权限：管理员)
    path('areas/all/', views.AreaList.as_view()),
    # 创建一个新大棚（区域）（权限：认证的用户）
    path('areas/new/', views.AreaCreate.as_view()),
    # 获得、更新、删除一个大棚（区域）实例（权限：管理者或者大棚拥有者）(按照大棚编号索引)
    path('areas/<int:pk>/', views.AreaDetail.as_view()),
    # 显示某用户的所有大棚（区域）列表（权限：认证的用户）（E.g. /areas_owner/1/    :显示id为1的用户的所有大棚（区域）列表）
    path('arealist/<int:pk>/', views.SpecificAreaList.as_view()),

    # 显示所有Arduino类型列表/创建一个新Arduino类型（权限：认证的用户）
    path('arduino_kinds/', views.KindOfArduinoList.as_view()),

    # 显示所有设备列表/新建一个设备
    path('devices/', views.DeviceList.as_view()),
    # 获得、更新、删除一个设备实例
    path('devices/<int:pk>/', views.DeviceDetail.as_view()),
    # 显示某大棚下的所有设备列表（E.g. /devicelist/1/    :显示id为1的大棚下的所有设备列表）
    path('devicelist/<int:pk>/', views.SpecificDeviceList.as_view()),

    # 显示所有iot数据列表/新建一个新iot数据
    path('agris/', views.AgriList.as_view()),
    # 获得、更新、删除一个iot数据实例
    path('agris/<int:pk>/', views.AgriDetail.as_view()),
    # 显示某Arduino产生的所有iot数据列表（E.g. /agrilist/1/    :显示id为1的Arduino下的所有iot数据列表）
    path('agrilist/<int:pk>/', views.SpecificAgriList.as_view()),
    # 显示某Arduino所产生的最新的n条iot数据列表（E.g. /agrilist/1/1/    :显示id为1的Arduino下的最新的一条iot数据列表）
    path('agrilist/<int:pk>/<int:number>/', views.LimitAgriList.as_view()),


    # # 显示所有树莓派列表/创建一个新树莓派节点
    # path('rbplist/', views.RaspberryPiList.as_view()),
    # # 显示某大棚（区域）内的所有树莓派列表（E.g. /rbplist/1/    :显示编号为1的大棚（区域）内所有的树莓派列表）
    # path('rbplist/<int:number>/', views.SpecificRaspberryPiList.as_view()),

    #
    # # 显示所有Arduino设备列表/创建一个新Arduino设备
    # path('ardlist/', views.ArduinoList.as_view()),
    # # 显示某大棚（区域）下的所有Arduino设备列表
    # # (E.g. /arduinodevicelist/1/ :显示编号为1的大棚（区域）内所有的Arduino设备）
    # path('areaofardlist/<int:number_area>/', views.SpecificAreaArduinoList.as_view()),
    # # # 显示某大棚（区域）下的某个树莓派下的所有Arduino设备列表
    # # # (E.g. /arduinodevicelist/1/2/ :显示编号为1的大棚（区域）下编号为2的树莓派的所有的Arduino设备）
    # # path('arduinodevicelist/<int:number_area>/<int:number_rbp>', views.SpecificAreaRbpArduinoDeviceList.as_view()),
    # # 显示某个树莓派下的所有Arduino设备列表
    # # (E.g. /rbpofardlist/1/ :显示编号为1的树莓派下的所有的Arduino设备）
    # path('rbpofardlist/<int:number_rbp>/', views.SpecificRbpArduinoList.as_view()),
    #
    # # 显示所有Arduino产生的iot数据列表/创建一个新的iot的数据
    # path('agrilist/', views.AgriList.as_view()),
    # # 显示某大棚（区域）下所有的iot数据列表
    # # (E.g. /areaofagrilist/1/ :显示编号为1的大棚（区域）下所有的iot数据）
    # path('areaofagrilist/<int:number_area>/', views.SpecificAreaAgriList.as_view()),
    # # 显示某树莓派下所有的iot数据列表
    # # (E.g. /rbpofagrilist/1/ :显示编号为1的树莓派下所有的iot数据）
    # path('rbpofagrilist/<int:number_rbp>/', views.SpecificRbpAgriList.as_view()),
    # # 显示某Arduino下所有的iot数据列表
    # # (E.g. /ardofagrilist/1/ :显示编号为1的Arduino下所有的iot数据）
    # path('ardofagrilist/<int:number_ard>/', views.SpecificArdAgriList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

