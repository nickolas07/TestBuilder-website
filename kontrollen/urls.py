from django.urls import path
from . import views

urlpatterns = [
    path('', views.kontrollen, name='kontrollen'),
    path('<str:identifier>/', views.view, name='view_kontrolle'),
    path('pdf/<str:identifier>/', views.pdf, name='view_pdf'),
    path('beispiel/<str:identifier>/', views.beispiel, name='view_beispiel'),
    path('download/<str:identifier>/', views.download, name='download_pdf'),
    path('probe/<str:identifier>/', views.probe_erstellen, name='kontrolle_erstellen'),
    path('erstellen/<str:identifier>/', views.kontrolle_erstellen, name='kontrolle_erstellen'),
    path('erstellen/<str:identifier>/<str:aufgaben>/', views.kontrolle_erstellen, name='kontrolle_erstellen_konfigo'),
]
