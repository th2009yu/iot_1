from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    # 客户端命令接口
    path('order', views.order),

    # 用户模块#################################
    # 用户注册（权限：所有人）
    path('register/', views.UserRegister.as_view()),
    # 用户登录（权限：所有人）
    path('login/', views.UserLogin.as_view()),
    # 用户登出
    path('logout/', views.user_logout),
    # 显示所有用户列表（权限：管理员）
    path('users/all/', views.UserList.as_view()),
    # 获取、更新或删除某个用户实例（权限：管理员）
    path('users/<int:pk>/', views.UserDetail.as_view()),

    # 大棚(区域)模块#################################
    # 显示所有大棚(区域)列表(权限：管理员)
    path('areas/all/', views.AreaList.as_view()),
    # 创建一个新大棚（区域）（权限：认证的用户）
    path('areas/new/', views.AreaCreate.as_view()),
    # 获得、更新、删除一个大棚（区域）实例（权限：管理者或者大棚拥有者）
    path('areas/<int:pk>/', views.AreaDetail.as_view()),
    # 显示某用户的所有大棚（区域）列表（权限：认证的用户）（E.g. /arealist/1/    :显示id为1的用户的所有大棚（区域）列表）
    path('arealist/<int:pk>/', views.SpecificAreaList.as_view()),

    # 显示所有Arduino类型列表/创建一个新Arduino类型（权限：认证的用户）
    path('arduino_kinds/', views.KindOfArduinoList.as_view()),

    # 设备模块#################################
    # 显示所有设备列表（权限：管理员）
    path('devices/all/', views.DeviceList.as_view()),
    # 新建一个设备（权限：认证的用户）
    path('devices/new/', views.DeviceCreate.as_view()),
    # 获得、更新、删除一个设备实例（权限：认证的用户）
    path('devices/<int:pk>/', views.DeviceDetail.as_view()),
    # 显示某大棚下的所有设备列表（权限：认证的用户）（E.g. /devicelist/1/    :显示id为1的大棚下的所有设备列表）
    path('devicelist/<int:pk>/', views.SpecificDeviceList.as_view()),

    # iot数据模块#################################
    # 显示所有iot数据列表(权限：管理员)
    path('agris/all/', views.AgriList.as_view()),
    # 新建一个新iot数据(权限：认证的用户)
    path('agris/new/', views.AgriCreate.as_view()),
    # 获得、更新、删除一个iot数据实例（权限：认证的用户）
    path('agris/<int:pk>/', views.AgriDetail.as_view()),
    # 显示某Arduino产生的所有iot数据列表（权限：认证的用户）（E.g. /agrilist/1/    :显示id为1的Arduino下的所有iot数据列表）
    path('agrilist/<int:pk>/', views.SpecificAgriList.as_view()),
    # 显示某Arduino所产生的最新的n条iot数据列表(权限：认证的用户)(E.g. /agrilist/1/1/:显示id为1的Arduino下的最新的一条iot数据列表）
    path('agrilist/<int:pk>/<int:number>/', views.LimitAgriList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

