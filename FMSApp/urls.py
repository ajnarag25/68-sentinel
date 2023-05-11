from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login, name='login'),
    path('login', views.login, name='login'),
    path('main_menu', views.main_menu, name='main_menu'),
    path('logout', views.logout, name='logout'),
    path('Input_VDetails', views.Input_VDetails, name='Input_VDetails'),
    path('Input_VSpecs', views.Input_VSpecs, name='Input_VSpecs'),
    path('SearchResults', views.SearchResults, name='SearchResults'),
    path('SearchPage', views.SearchPage, name='SearchPage'),
    path('Vdetails', views.Vdetails, name='Vdetails'),
    path('Vspecs', views.Vspecs, name='Vspecs'),
    path('Ddetails', views.Ddetails, name='Ddetails'),
    path('Input_DDetails', views.Input_DDetails, name='Input_DDetails'),
    path('Input_MSched', views.Input_MSched, name='Input_MSched'),
    path('Update_VDetailsPage/<int:pk>/', views.Update_VDetailsPage, name='Update_VDetailsPage'),
    path('Update_VSpecsPage/<int:pk>/', views.Update_VSpecsPage, name='Update_VSpecsPage'),
    path('Update_DDetailsPage/<int:pk>/', views.Update_DDetailsPage, name='Update_DDetailsPage'),
    path('deleteDDetailButton/<int:pk>/', views.deleteDDetailButton, name='deleteDDetailButton'),
    path('exportVDetails', views.exportVDetails, name='exportVDetails'),
    path('exportDDetails', views.exportDDetails, name='exportDDetails'),
    path('exportVSpecs', views.exportVSpecs, name='exportVSpecs'),
    path('FilteredSearchResults', views.FilteredSearchResults, name='FilteredSearchResults'),
    path('MSchedPage', views.MSchedPage, name='MSchedPage'),
    path('DeploymentPage', views.DeploymentPage, name='DeploymentPage'),
    path('Input_Deployment', views.Input_Deployment, name='Input_Deployment'),
    path('Update_Deployment/<int:pk>/', views.Update_Deployment, name='Update_Deployment'),
    path('exportDeployment', views.exportDeployment, name='exportDeployment'),
    path('Update_Maintenance/<int:pk>/', views.Update_Maintenance, name='Update_Maintenance'),
    path('exportMaintenance', views.exportMaintenance, name='exportMaintenance'),
]
