from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path('addr_from_id_list/', views.addr_from_id_list, name='addr_from_id_list'),
    path('addr_select/', views.addr_select, name='addr_select'),
    path('addr_table_json/', views.addr_table_json, name='addr_table_json'),
    path('addr_table/', views.addr_table, name='addr_table'),
    path('get_house_id/', views.get_house_id, name='get_house_id'),
    path('get_houses_numbers/<slug:addr_id>/', views.get_houses_numbers, name='get_houses_numbers'),

    path('working_day_year/<int:year>/', views.working_day_year, name='working_day_year'),
    path('working_day_year/', views.working_day_year, name='working_day_year'),
    path('working_day_calendar/', views.working_day_calendar, name='working_day_calendar'),
    path('working_day_change/', views.working_day_change, name='working_day_change'),
    path('calculate_date/', views.calculate_date, name='calculate_date'),

    path('org_json_list/', views.org_json_list, name='org_json_list'),
    path('org_json_table/', views.org_json_table, name='org_json_table'),
    path('org_table/', views.org_table, name='org_table'),
    path('org_form/new/', views.new_org_form, name='new_org_form'),
    path('org_form/save/', views.org_form_save, name='org_form_save'),
    path('org_form/<slug:id>/', views.edit_org_form, name='edit_org_form'),

    path('house_json_table/', views.house_json_table, name='house_json_table'),
    path('house_table/', views.house_table, name='house_table'),
    path('house_form/new/', views.new_house_form, name='new_house_form'),
    path('house_form/save/', views.house_form_save, name='house_form_save'),
    path('house_form/<slug:id>/', views.edit_house_form, name='edit_house_form'),

    path('delete_document/', views.delete_document, name='delete_document'),

]
