from django.urls import path
from . import views

urlpatterns = [
    path('', views.tests, name='tests'),
    path('<str:identifier>/', views.view, name='view_test'),
    path('pdf/<str:identifier>/', views.pdf, name='view_pdf'),
    path('beispiel/<str:identifier>/', views.beispiel, name='view_beispiel'),
    path('download/<str:identifier>/', views.download, name='download_pdf'),
    path('probe/<str:identifier>/', views.probe_erstellen, name='test_erstellen'),
    path('erstellen/<str:identifier>/', views.test_erstellen, name='test_erstellen'),
    path('erstellen/<str:identifier>/<str:aufgaben>/', views.test_erstellen, name='test_erstellen_aufgaben'),
]
