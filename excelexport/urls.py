from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('countries_gdp_list/', views.countries_gdp_list, name='countries_gdp_list'),
    path('countries_gdp_excel/', views.countries_gdp_excel, name='countries_gdp_excel'),
    path('advanced_materials_testing/', views.advanced_materials_testing, name='advanced_materials_testing'),
    path('analysis_results/', views.analysis_results, name='analysis_results'),
    path('mechanical-inspection/', views.mechanical_inspection_report, name='mechanical_inspection_report'),
    path('reset-database/', views.reset_database, name='reset_database'),
    path('user-login/', views.user_login, name='user_login'),
]