from django.urls import path
from . import views

urlpatterns = [
    path('', views.suchen, name='kontrolle_suchen'),
    path('notFound/', views.not_found, name='nicht_gefunden'),
    path('delete/<str:name>/', views.delete, name='delete'),
]