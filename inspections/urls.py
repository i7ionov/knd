from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path('inspection_table/', views.inspection_table, name='inspection_table'),
    path('inspection_form/new/', views.new_inspection_form, name='new_inspection_form'),
    path('inspection_form/save/', views.inspection_form_save, name='inspection_form_save'),
    # path('inspection_form/<int:id>/', None, name='inspection_form'),
]
