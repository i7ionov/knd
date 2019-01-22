from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path('inspection_table/', views.inspection_table, name='inspection_table'),
    path('inspection_form/new/', views.new_inspection_form, name='new_inspection_form'),
    path('inspection_form/save/', views.inspection_form_save, name='inspection_form_save'),
    path('inspection_form/<slug:id>/', views.edit_inspection_form, name='edit_inspection_form'),
    path('violation_in_inspection_json_list/<slug:id>/', views.violation_in_inspection_json_list, name='violation_in_inspection_json_list'),
    path('inspection_json_table/', views.inspection_json_table, name='inspection_json_table'),
]
