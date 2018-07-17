from django.urls import path
from . import views
# from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    # 客户端命令接口
    path('order', views.order),

    # 显示所有用户列表/创建一个新用户
    path('ownerlist/', views.OwnerList.as_view()),

    # 显示所有大棚列表/创建一个新大棚
    path('arealist/', views.AreaList.as_view()),
    # 显示某用户的所有大棚列表（E.g. /arealist/aaa/    :显示aaa用户的所有大棚列表）
    path('arealist/<str:name>/', views.SpecificAreaList.as_view()),

    # 显示所有田野的所有数据列表/创建一个新田野
    path('field/', views.FieldList.as_view()),
    # 查询某田野大棚的所有数据列表,按数据创建时间顺序排序（E.g. /field/1/     : 田野一号大棚的所有数据）
    path('field/<int:number>/', views.SpecificFieldList.as_view()),
    # 查询某田野大棚的一定长度的数据列表,按数据创建时间顺序排序 （E.g. /field/1/100/     : 田野一号大棚的100条数据）
    path('field/<int:number>/<int:length>/', views.SpecificLimitFieldList.as_view()),

    # 显示所有池塘的所有数据列表/创建一个新池塘
    path('pond/', views.PondList.as_view()),
    # 查询某池塘大棚的所有数据列表,按数据创建时间顺序排序（E.g. /pond/1/     : 池塘一号大棚的所有数据）
    path('pond/<int:number>/', views.SpecificPondList.as_view()),
    # 查询某池塘大棚的一定长度的数据列表,按数据创建时间顺序排序 （E.g. /pond/1/100/     : 池塘一号大棚的100条数据）
    path('pond/<int:number>/<int:length>/', views.SpecificLimitPondList.as_view()),

    # 显示所有森林的所有数据列表/创建一个新森林
    path('forest/', views.ForestList.as_view()),
    # 查询某森林大棚的所有数据列表,按数据创建时间顺序排序（E.g. /forest/1/     : 森林一号大棚的所有数据）
    path('forest/<int:number>/', views.SpecificForestList.as_view()),
    # 查询某森林大棚的一定长度的数据列表,按数据创建时间顺序排序 （E.g. /forest/1/100/     : 池塘一号大棚的100条数据）
    path('forest/<int:number>/<int:length>/', views.SpecificLimitForestList.as_view()),
]

# urlpatterns = format_suffix_patterns(urlpatterns)

