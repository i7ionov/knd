from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path('general_report_table/', views.general_report_table, name='general_report_table'),
    path('general_report_table_json/', views.general_report_table_json, name='general_report_table_json'),
    path('general_report_form/<slug:id>/', views.general_report_form, name='general_report_form'),
    path('new_general_report/', views.new_general_report, name='new_general_report'),

]
