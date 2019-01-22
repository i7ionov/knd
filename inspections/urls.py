from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path('inspection_table/', views.inspection_table, name='inspection_table'),
    path('inspection_form/new/', views.new_inspection_form, name='new_inspection_form'),
    path('inspection_form/save/', views.inspection_form_save, name='inspection_form_save'),
    path('violation_in_inspection_json_list/<slug:id>/', views.violation_in_inspection_json_list, name='violation_in_inspection_json_list'),
]
