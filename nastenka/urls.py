from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('nastenka/', views.nastenka, name='nastenka'),
    path('kontakty/', views.kontakty, name='kontakty'),
    path('zakladni-info/', views.zakladni_info, name='zakladni-info'),
]
