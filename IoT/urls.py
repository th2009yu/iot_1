from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    # 手动控制 (E.g. /order?area_number=1&ard_mac=11111&command=hhh)
    path('order', views.order.as_view()),


    # 用户模块#################################
    # 用户注册
    path('register/', views.UserRegister.as_view()),
    # 用户登录
    path('login/', views.UserLogin.as_view()),
    # 用户登出
    path('logout/', views.user_logout),
    # 显示所有用户列表
    path('users/all/', views.UserList.as_view()),
    # 获得GET、更新PUT、删除DELETE某个用户实例，(E.g. /users/1/ :获取、更新或删除用户id为1的实例)
    path('users/<int:pk>/', views.UserDetail.as_view()),


    # 大棚管理模块#################################
    # 显示所有大棚列表
    path('areas/all/', views.AreaList.as_view()),
    # 创建一个新大棚
    path('areas/new/', views.AreaCreate.as_view()),
    # 获得GET、更新PUT、删除DELETE某个大棚实例，修改阈值信息(E.g. /areas/1/ :获取、更新或删除大棚编号为1的实例)
    path('areas/<int:pk>/', views.AreaDetail.as_view()),
    # 显示当前用户的所有大棚列表
    path('arealist/', views.SpecificAreaList.as_view()),
    # 创建一个新大棚及其设备
    path('areas-devices/new/', views.AreaDeviceCreate.as_view()),
    # 获得GET一个大棚实例及其设备列表 (E.g. /areas-devices-get/1/ :获取大棚编号为1的实例及该大棚下的设备列表)
    path('areas-devices-get/<int:pk>/', views.AreaDeviceDetailGet.as_view()),
    # 修改大棚信息以及该大棚下的设备(E.g. /areas-devices-modify/1/ :修改大棚编号为1的实例及该大棚下的设备)
    path('areas-devices-modify/<int:pk>', views.AreaDeviceDetailModify.as_view()),
    # 获取某大棚详情信息：其中包括大棚信息、及其设备信息、以及每个设备的最新的一条传感器数据、设备控制的数据、报警记录数据（pk指代大棚编号）
    path('areas-devices-show/<int:pk>/', views.AreaDeviceDetailShow.as_view()),
    # 获取当前用户的大棚数量、arduino数量、报警记录的数量
    path('areas-devices-alarms-count/', views.AreaDeviceAlarmCount.as_view()),


    # 设备模块#################################
    # 显示所有设备列表
    path('devices/all/', views.DeviceList.as_view()),
    # 新建一个设备
    path('devices/new/', views.DeviceCreate.as_view()),
    # 获得GET、更新PUT、删除DELETE一个设备实例(E.g. /devices/ardmac111/ :获取、更新或删除Ard_mac地址为ardmac111的实例)
    path('devices/<str:pk>/', views.DeviceDetail.as_view()),
    # 显示某大棚下的所有设备列表（E.g. /devicelist/1/    :显示id为1的大棚下的所有设备列表）
    path('devicelist/<int:pk>/', views.SpecificDeviceList.as_view()),
    # 显示所有设备类型列表/创建一个新设备类型
    # path('device_kinds/', views.KindOfArduinoList.as_view()),


    # iot数据模块#################################
    # 显示所有iot数据列表
    path('agris/all/', views.AgriList.as_view()),
    # 传感器数据与控制设备开关数据的接收(新建iot数据与设备的控制开关数据)与阈值返回
    path('agris/new/', views.AgriCreate),
    # 获得GET、更新PUT、删除DELETE一个iot数据实例(E.g. /agris/1/    :获取、更新或删除id为1的iot数据）
    path('agris/<int:pk>/', views.AgriDetail.as_view()),
    # 显示某Arduino产生的所有iot数据列表（E.g. /agrilist/ardmac111/ :显示ard_mac为ardmac111的Arduino下的所有iot数据列表）
    path('agrilist/<str:pk>/', views.SpecificAgriList.as_view()),
    # 显示某Arduino所产生的最新的n条iot数据列表(E.g. /agrilist/ardmac111/1/:显示ard_mac为ardmac111的Arduino下的最新的1条iot数据列表）
    path('agrilist/<str:pk>/<int:number>/', views.LimitAgriList.as_view()),
    # 显示某大棚下所有iot数据列表（E.g. /agrilist-area/1/ :显示编号为1的大棚下所有iot数据列表）
    path('agrilist-area/<int:pk>/', views.SpecificAgriListArea.as_view()),
    # 显示某大棚下所产生的最新的n条iot数据列表(E.g. /agrilist-area/1/1/ :显示大棚编号为1下最新的1条iot数据列表)
    path('agrilist-area/<int:pk>/<int:number>/', views.LimitAgriListArea.as_view()),


    # 报警记录模块################################
    # 显示所有报警记录列表
    path('alarms/all/', views.AlarmList.as_view()),
    # 报警记录接收（新建一个报警记录）
    path('alarms/new/', views.AlarmCreate),
    # 获得GET、更新PUT、删除DELETE某个报警记录实例，(E.g. /alarms/1/ :获取、更新或删除报警记录id为1的实例)
    path('alarms/<int:pk>/', views.AlarmDetail.as_view()),
    # 显示某大棚下的所有报警记录列表（pk：大棚id）
    path('alarmlist/<int:pk>/', views.SpecificAlarmList.as_view()),
    # 显示某大棚下的所有的最新的n条报警记录列表(E.g. /alarmlist/1/1/:显示大棚编号为1的大棚下的最新的1条报警记录列表）
    path('alarmlist/<int:pk>/<int:number>/', views.LimitAlarmList.as_view()),
    # 显示某Arduino下的所有报警记录列表（E.g. /alarmlist-ard/ardmac111/ :显示ard_mac为ardmac111的arduino下的所有报警记录列表）
    path('alarmlist-ard/<str:pk>/', views.SpecificAlarmListArd.as_view()),
    # 显示某Arduino下的所有的最新的n条报警记录列表（E.g. /alarmlist-ard/ardmac111/1/ :显示ard_mac为ardmac111的arduino下的最新的1条报警记录列表）
    path('alarmlist-ard/<str:pk>/<int:number>/', views.LimitAlarmListArd.as_view()),
    # 显示当前用户下所有的报警记录,其中包括大棚名称+Ard_MAC+报警内容+报警记录产生时间以及结束时间
    path('alarmlist-user/', views.SpecificAlarmListUser.as_view()),
    # 根据条件刷选来获取报警记录列表(E.g. /alarmlist-condition?area_number=1&ard_mac=00-00-01&time=232322)
    path('alarmlist-condition', views.AlarmListCondition.as_view()),


    # 历史数据模块###############################
    # 查看当前用户所有的大棚ID、名称以及各个大棚下Arduino的MAC地址
    path('areas-devices-list/', views.AreaDeviceList.as_view()),
    # 根据设备的MAC地址，获取某天的数据,pk为Arduino的MAC地址，timestamp为当天的时间戳
    path('history-iot/<str:pk>/<int:timestamp>', views.HistoryIoT.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)

