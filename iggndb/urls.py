"""iggndb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('dict/', include('dictionaries.urls')),
    path('insp/', include('inspections.urls')),
    path('ad/', include('ad.urls')),
    path('fssp/', include('fssp.urls')),
    path('analytic/', include('analytic.urls')),
    path('', views.index, name='index'),
    path('history_table/', views.history_table, name='history_table'),
    path('history_form/<slug:model>/<int:id>/<int:history_id>/', views.history_form, name='history_form'),
    path('document_tree_json/<int:id>/', views.document_tree_json, name='document_tree_json'),
    path('document_tree/', views.document_tree, name='document_tree'),
    path('files_list/', views.files_list, name='files_list'),
    path('file_select/', views.file_select, name='file_select'),
    path('file_add/', views.file_add, name='file_add'),
    path('save_preference/', views.save_preference, name='save_preference'),
]
