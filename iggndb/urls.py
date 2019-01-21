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
    # path('ad/', include('ad.urls')),
    # path('analytic/', include('analytic.urls')),
    path('', views.index, name='index'),
    # path('history_table/', views.history_table, name='history_table'),
    # path('history_card/<int:id>/<int:history_id>/', views.history_card, name='history_card'),
]
