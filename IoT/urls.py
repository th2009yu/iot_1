from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    # 客户端命令接口
    path('order', views.order),

    # 用户模块#################################
    # 用户注册
    path('register/', views.UserRegister.as_view()),
    # 用户登录
    path('login/', views.UserLogin.as_view()),
    # 用户登出
    path('logout/', views.user_logout),
    # List all users
    path('users/all/', views.UserList.as_view()),
    # Retrieve a user instance.（按照用户id索引）
    path('users/<int:pk>/', views.UserDetail.as_view()),

    # 大棚(区域)模块#################################
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

    # 设备模块#################################
    # 显示所有设备列表
    path('devices/all/', views.DeviceList.as_view()),
    # 新建一个设备
    path('devices/new/', views.DeviceCreate.as_view()),
    # 获得、更新、删除一个设备实例
    path('devices/<int:pk>/', views.DeviceDetail.as_view()),
    # 显示某大棚下的所有设备列表（E.g. /devicelist/1/    :显示id为1的大棚下的所有设备列表）
    path('devicelist/<int:pk>/', views.SpecificDeviceList.as_view()),

    # iot数据模块#################################
    # 显示所有iot数据列表/新建一个新iot数据
    path('agris/all/', views.AgriList.as_view()),
    # 新建一个新iot数据
    path('agris/new/', views.AgriCreate.as_view()),
    # 获得、更新、删除一个iot数据实例
    path('agris/<int:pk>/', views.AgriDetail.as_view()),
    # 显示某Arduino产生的所有iot数据列表（E.g. /agrilist/1/    :显示id为1的Arduino下的所有iot数据列表）
    path('agrilist/<int:pk>/', views.SpecificAgriList.as_view()),
    # 显示某Arduino所产生的最新的n条iot数据列表（E.g. /agrilist/1/1/    :显示id为1的Arduino下的最新的一条iot数据列表）
    path('agrilist/<int:pk>/<int:number>/', views.LimitAgriList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

