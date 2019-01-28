from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path('ad_record_form/new/<int:ad_type>/<slug:parent_id>/<int:stage_id>/', views.new_ad_record_form, name='new_ad_record_form'),
    path('ad_record_form/save/', views.ad_record_form_save, name='ad_record_form_save'),
    path('ad_record_form/<slug:id>/', views.edit_ad_record_form, name='edit_ad_record_form'),

]
