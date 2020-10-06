from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('result/', views.result, name='result'),
    path('result/regenerate/', views.regenerate, name='regenerate'),
    path('result/download/', views.download, name='download'),
]
