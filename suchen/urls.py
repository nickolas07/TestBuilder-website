from django.urls import path
from . import views

urlpatterns = [
    path('', views.suchen, name='test_suchen'),
    path('nicht-gefunden/', views.not_found, name='nicht_gefunden'),
    path('delete/<str:name>/', views.delete, name='delete'),
]