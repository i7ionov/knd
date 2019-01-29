from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path('addr_from_id_list/', views.addr_from_id_list, name='addr_from_id_list'),
    path('addr_select/', views.addr_select, name='addr_select'),
    path('addr_table_json/', views.addr_table_json, name='addr_table_json'),
    path('addr_table/', views.addr_table, name='addr_table'),
    path('get_house_id/', views.get_house_id, name='get_house_id'),

    path('files_list/', views.files_list, name='files_list'),
    path('file_select/', views.file_select, name='file_select'),
    path('file_add/', views.file_add, name='file_add'),

    path('working_day_year/<int:year>/', views.working_day_year, name='working_day_year'),
    path('working_day_year/', views.working_day_year, name='working_day_year'),
    path('working_day_calendar/', views.working_day_calendar, name='working_day_calendar'),
    path('working_day_change/', views.working_day_change, name='working_day_change'),
    path('calculate_date/', views.calculate_date, name='calculate_date'),

    path('org_json_list/', views.org_json_list, name='org_json_list'),

]
