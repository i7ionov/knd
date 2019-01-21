from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path('addr_from_id_list/', views.addr_from_id_list, name='addr_from_id_list'),
    path('addr_select/', views.addr_select, name='addr_select'),
    path('addr_table_json/', views.addr_table_json, name='addr_table_json'),
    path('addr_table/', views.addr_table, name='addr_table'),
    path('get_house_id/', views.get_house_id, name='get_house_id'),
]