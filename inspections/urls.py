from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path('inspection_table/', views.inspection_table, name='inspection_table'),
]
