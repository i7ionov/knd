from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path('fssp_query_form/', views.fssp_query_form, name='fssp_query_form'),
    path('fssp_search_legal/', views.fssp_search_legal, name='fssp_search_legal'),
    path('requests_table/', views.requests_table, name='requests_table'),
    path('request_json_table/', views.request_json_table, name='request_json_table'),
    path('result/', views.result, name='result'),
    path('response/<slug:id>/', views.response, name='response'),
]
