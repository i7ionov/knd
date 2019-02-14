from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path('general_report_table/', views.general_report_table, name='general_report_table'),
    path('general_report_table_json/', views.general_report_table_json, name='general_report_table_json'),
    path('general_report_form/<slug:id>/', views.general_report_form, name='general_report_form'),
    path('new_general_report/', views.new_general_report, name='new_general_report'),

    path('excel_export_table/', views.excel_export_table, name='excel_export_table'),
    path('filter_form/', views.filter_form, name='filter_form'),
    path('field_filter_form/', views.field_filter_form, name='field_filter_form'),
    path('generic_json_list/', views.generic_json_list, name='generic_json_list'),
]
