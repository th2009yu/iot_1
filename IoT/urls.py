from django.urls import path
from . import views
# from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    # 客户端命令接口
    path('order', views.order),

    # 显示所有用户列表/创建一个新用户
    path('ownerlist/', views.OwnerList.as_view()),

    # 显示所有大棚（区域）列表/创建一个新大棚（区域）
    path('arealist/', views.AreaList.as_view()),
    # 显示某用户的所有大棚（区域）列表（E.g. /arealist/aaa/    :显示aaa用户的所有大棚（区域）列表）
    path('arealist/<str:name>/', views.SpecificAreaList.as_view()),

    # 显示所有树莓派列表/创建一个新树莓派节点
    path('rbplist/', views.RaspberryPiList.as_view()),
    # 显示某大棚（区域）内的所有树莓派列表（E.g. /rbplist/1/    :显示编号为1的大棚（区域）内所有的树莓派列表）
    path('rbplist/<int:number>/', views.SpecificRaspberryPiList.as_view()),

    # 显示所有Arduino类型列表/创建一个新Arduino类型
    path('kindofard/', views.KindOfArduinoList.as_view()),

    # 显示所有Arduino设备列表/创建一个新Arduino设备
    path('ardlist/', views.ArduinoList.as_view()),
    # 显示某大棚（区域）下的所有Arduino设备列表
    # (E.g. /arduinodevicelist/1/ :显示编号为1的大棚（区域）内所有的Arduino设备）
    path('areaofardlist/<int:number_area>/', views.SpecificAreaArduinoList.as_view()),
    # # 显示某大棚（区域）下的某个树莓派下的所有Arduino设备列表
    # # (E.g. /arduinodevicelist/1/2/ :显示编号为1的大棚（区域）下编号为2的树莓派的所有的Arduino设备）
    # path('arduinodevicelist/<int:number_area>/<int:number_rbp>', views.SpecificAreaRbpArduinoDeviceList.as_view()),
    # 显示某个树莓派下的所有Arduino设备列表
    # (E.g. /rbpofardlist/1/ :显示编号为1的树莓派下的所有的Arduino设备）
    path('rbpofardlist/<int:number_rbp>/', views.SpecificRbpArduinoList.as_view()),

    # 显示所有Arduino产生的iot数据列表/创建一个新的iot的数据
    path('agrilist/', views.AgriList.as_view()),
    # 显示某大棚（区域）下所有的iot数据列表
    # (E.g. /areaofagrilist/1/ :显示编号为1的大棚（区域）下所有的iot数据）
    path('areaofagrilist/<int:number_area>/', views.SpecificAreaAgriList.as_view()),
    # 显示某树莓派下所有的iot数据列表
    # (E.g. /rbpofagrilist/1/ :显示编号为1的树莓派下所有的iot数据）
    path('rbpofagrilist/<int:number_rbp>/', views.SpecificRbpAgriList.as_view()),
    # 显示某Arduino下所有的iot数据列表
    # (E.g. /ardofagrilist/1/ :显示编号为1的Arduino下所有的iot数据）
    path('ardofagrilist/<int:number_ard>/', views.SpecificArdAgriList.as_view()),
]

# urlpatterns = format_suffix_patterns(urlpatterns)

