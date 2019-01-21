from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path('addr_from_id_list/', views.addr_from_id_list, name='addr_from_id_list'),
    path('addr_select/', views.addr_select, name='addr_select'),

]
